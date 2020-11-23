from datetime import datetime
from itertools import groupby
from typing import Callable, List, Optional, Iterator

from raspberry_home.assets import Assets
from raspberry_home.controller.input_controller import NavigationItem
from raspberry_home.controller.utils.moon import MoonPhase, Moon
from raspberry_home.controller.utils.sun import Sun
from raspberry_home.display.display import Display
from raspberry_home.platform.characteristic import Characteristic, Characteristics
from raspberry_home.platform.measurement import Measurement
from raspberry_home.platform.measurements_scheduler import MeasurementsListener
from raspberry_home.platform.sensor import Sensor
from raspberry_home.sensor.covid19monitor import COVID19Monitor
from raspberry_home.view.center import Center
from raspberry_home.view.font import Font, FontWeight
from raspberry_home.view.geometry import Size, Point
from raspberry_home.view.GridWidget import GridWidget
from raspberry_home.view.image import Image
from raspberry_home.view.offset import Offset
from raspberry_home.view.render import FixedSizeRender, ColorSpace
from raspberry_home.view.stack import HorizontalStack, VerticalStack, StackDistribution, StackAlignment
from raspberry_home.view.text import Text
from raspberry_home.view.view import View
from raspberry_home.view.widget import Widget


class Fonts:
    timeFont = Font(32, FontWeight.BOLD)
    dateFont = Font(18, FontWeight.MEDIUM)
    valueFont = Font(15, FontWeight.MEDIUM)
    sunTimeFont = Font(12, FontWeight.MEDIUM)


class HomeController(MeasurementsListener, NavigationItem):

    def __init__(self, display: Display, coordinates, timezone_offset):
        self.display = display
        self.coordinates = coordinates
        self.timezone_offset = timezone_offset

    def selected_show(self):
        pass

    def on_measurements(self, measurements: List[Measurement]):
        self.display_measurements(measurements)

    def display_measurements(self, measurements: List[Measurement]):
        cells = [
            # First Row
            NowCell(
                timezone_offset=self.timezone_offset,
                sun=Sun(coords=self.coordinates),
                moon=Moon(),
            ),
            self._get_measurements_cell([Characteristics.temperature], measurements),
            self._get_measurements_cell([Characteristics.pressure], measurements),
            # Second Row
            self._get_measurements_cell([Characteristics.wind_speed, Characteristics.wind_direction], measurements,
                                        only_primary=False),
            None,
            self._get_measurements_cell([Characteristics.virusCases], measurements)
        ]

        self.display.set_view(
            root_view=GridWidget.from_list(columns=3, rows=2, cells=cells)
        )

    def _get_measurements_cell(
            self,
            of_types: List[Characteristic],
            measurements: List[Measurement],
            only_primary: bool = True
    ) -> View:
        measurements = list(filter(
            lambda m: m.characteristic.name in map(lambda t: t.name, of_types) and (not only_primary or m.is_primary()),
            measurements))
        return MeasurementsCell(measurements) if len(measurements) > 0 else None


class NowCell(Widget):

    def __init__(self, timezone_offset, sun: Sun, moon: Moon):
        self.timezone_offset = timezone_offset
        self.sun = sun
        self.moon = moon

    def build(self) -> View:
        now = datetime.now()
        time = now.strftime("%H:%M")
        date = now.strftime("%d.%m")

        return Center(VerticalStack(
            alignment=StackAlignment.Center,
            children=[
                Text(time, font=Fonts.timeFont),
                Offset(
                    offset=Point(0, -6),
                    child=Text(date, font=Fonts.dateFont),
                ),
                Offset(
                    offset=Point(0, -2),
                    child=self._build_moon_and_sun(),
                )
            ]
        ))

    def _build_moon_and_sun(self):
        sun_rise = self.time_to_text(self.sun.get_sunrise_time())
        sun_set = self.time_to_text(self.sun.get_sunset_time())
        return HorizontalStack(
            spacing=8,
            alignment=StackAlignment.Center,
            children=[
                Image(self._get_moon_phase_filename()),
                VerticalStack([
                    HorizontalStack([
                        Image(Assets.Images.sunrise),
                        Text(sun_rise, font=Fonts.sunTimeFont)
                    ], spacing=3),
                    HorizontalStack([
                        Image(Assets.Images.sunset),
                        Text(sun_set, font=Fonts.sunTimeFont)
                    ], spacing=3)
                ])
            ]
        )

    def time_to_text(self, time):
        shifted_time = time['decimal'] + self.timezone_offset / 3600
        return "%s:%s" % (int(shifted_time), int(shifted_time % 1.0 * 60))

    @staticmethod
    def _get_moon_phase_filename():
        phase = Moon().get_phase()
        return {
            MoonPhase.NEW_MOON: Assets.Images.moon_new_moon,
            MoonPhase.WAXING_CRESCENT: Assets.Images.moon_waxing_crescent,
            MoonPhase.FIRST_QUARTER: Assets.Images.moon_first_quarter,
            MoonPhase.WAXING_GIBBOUS: Assets.Images.moon_waxing_gibbous,
            MoonPhase.FULL_MOON: Assets.Images.moon_full_moon,
            MoonPhase.WANING_GIBBOUS: Assets.Images.moon_waning_gibbous,
            MoonPhase.LAST_QUARTER: Assets.Images.moon_last_quarter,
            MoonPhase.WANING_CRESCENT: Assets.Images.moon_waning_crescent,
        }[phase]


class MeasurementsCell(Widget):

    def __init__(self, measurements: [Measurement]):
        self.measurements = measurements

    def build(self) -> View:
        primary_measurement = self.measurements[0]
        icon = self._get_icon_filename(primary_measurement)
        value_text = "\n".join(map(lambda m: self._get_title(m), self.measurements))
        return Center(VerticalStack(
            spacing=4,
            alignment=StackAlignment.Center,
            children=[
                Image(icon, invert=False),
                Text(value_text, font=Fonts.valueFont, align=Text.Align.CENTER)
            ]
        ))

    @staticmethod
    def _get_icon_filename(measurement: Measurement):
        sensor = measurement.sensor
        characteristic = measurement.characteristic
        if characteristic == Characteristics.temperature:
            if sensor.has_flag("outside"):
                return Assets.Images.ic_temperature_outside
            else:
                return Assets.Images.ic_temperature
        elif characteristic == Characteristics.light:
            return Assets.Images.ic_day_and_night
        elif characteristic == Characteristics.pressure:
            return Assets.Images.ic_pressure_gauge
        elif characteristic == Characteristics.boolean:
            if sensor.has_flag("door"):
                return Assets.Images.ic_door_closed if measurement.value else Assets.Images.ic_door_open
            else:
                return Assets.Images.ic_boolean_true if measurement.value else Assets.Images.ic_boolean_false
        elif characteristic == Characteristics.humidity:
            return Assets.Images.ic_humidity
        elif characteristic == Characteristics.virusCases:
            return Assets.Images.ic_virus
        elif characteristic == Characteristics.soilMoisture:
            return Assets.Images.ic_flower
        elif characteristic == Characteristics.wind_speed or characteristic == Characteristics.wind_direction:
            return Assets.Images.ic_wind
        else:
            raise ValueError("Unknown characteristic: " + characteristic.name)

    @staticmethod
    def _get_title(measurement: Measurement):
        sensor = measurement.sensor
        characteristic = measurement.characteristic
        value = measurement.value
        if characteristic == Characteristics.boolean and sensor.has_flag("door"):
            return sensor.name
        if characteristic.name == "pressure":
            return str(round(value)) + " " + characteristic.unit
        elif isinstance(sensor, COVID19Monitor):
            return "{:,}".format(value[0]) + "\n" + "{:,}".format(value[1])
        else:
            return Sensor.formatted_value_with_unit(characteristic, value)
