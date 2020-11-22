from datetime import datetime
from typing import Callable, List

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
from raspberry_home.view.geometry import Size
from raspberry_home.view.image import Image
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
        width, height = self.display.get_size()
        render = FixedSizeRender(size=Size(width, height), color_space=ColorSpace.RGB)

        image = render.render(
            root_view=GridWidget(
                rows=2,
                columns=3,
                builder=lambda index, row, col: self._build_cell(index, row, col, measurements)
            ),
        )
        self.display.show(image)

    def _build_cell(self, index: int, row: int, column: int, measurements: List[Measurement]) -> View:
        if row == 0 and column == 0:
            return self._build_time_cell()
        else:
            index -= 1
            measurement = measurements[index]
            return self._build_measurement(measurement)

    def _build_time_cell(self) -> View:
        now = datetime.now()
        time = now.strftime("%H:%M")
        date = now.strftime("%d.%m")

        return Center(VerticalStack(
            alignment=StackAlignment.Center,
            children=[
                Text(time, font=Fonts.timeFont),
                Text(date, font=Fonts.dateFont),
                self._build_moon_and_sun(),
            ]
        ))

    def _build_moon_and_sun(self):
        sun = Sun()
        sun_rise = self.time_to_text(sun.calcSunTime(coords=self.coordinates, isRiseTime=True))
        sun_set = self.time_to_text(sun.calcSunTime(coords=self.coordinates, isRiseTime=False))
        return Center(HorizontalStack(
            spacing=4,
            alignment=StackAlignment.Center,
            children=[
                Image(self._get_moon_phase_filename()),
                VerticalStack([
                    HorizontalStack([
                        Image(Assets.Images.sunrise),
                        Text(sun_rise, font=Fonts.sunTimeFont)
                    ]),
                    HorizontalStack([
                        Image(Assets.Images.sunset),
                        Text(sun_set, font=Fonts.sunTimeFont)
                    ])
                ])
            ]
        ))

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

    def _build_measurement(self, measurement: Measurement) -> View:
        icon = self._get_icon_filename(measurement.sensor, measurement.characteristic, measurement.value)
        value_text = self._get_title(measurement.sensor, measurement.characteristic, measurement.value)
        return Center(VerticalStack(
            spacing=4,
            alignment=StackAlignment.Center,
            children=[
                Image(icon, invert=False),
                Text(value_text, font=Fonts.valueFont)
            ]
        ))

    @staticmethod
    def _get_icon_filename(sensor: Sensor, characteristic: Characteristic, value):
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
                return Assets.Images.ic_door_closed if value else Assets.Images.ic_door_open
            else:
                return Assets.Images.ic_boolean_true if value else Assets.Images.ic_boolean_false
        elif characteristic == Characteristics.humidity:
            return Assets.Images.ic_humidity
        elif characteristic == Characteristics.virusCases:
            return Assets.Images.ic_virus
        elif characteristic == Characteristics.soilMoisture:
            return Assets.Images.ic_flower
        else:
            raise ValueError("Unknown characteristic: " + characteristic.name)

    @staticmethod
    def _get_title(sensor: Sensor, characteristic: Characteristic, value):
        if characteristic == Characteristics.boolean and sensor.has_flag("door"):
            return sensor.name
        if characteristic.name == "pressure":
            return str(round(value)) + " " + characteristic.unit
        elif isinstance(sensor, COVID19Monitor):
            return "{:,}".format(value[0]) + "\n" + "{:,}".format(value[1])
        else:
            return Sensor.formatted_value_with_unit(characteristic, value)


class GridWidget(Widget):

    def __init__(self, columns: int, rows: int, builder: Callable[[int, int, int], View]):
        self.columns = columns
        self.rows = rows
        self.builder = builder

    def build(self) -> View:
        rows = []
        index = 0
        for row in range(0, self.rows):
            cells = []
            for column in range(0, self.columns):
                cell = self.builder(index, row, column)
                index += 1
                cells.append(cell)
            rows.append(HorizontalStack(
                distribution=StackDistribution.Equal,
                children=cells
            ))
        return VerticalStack(
            distribution=StackDistribution.Equal,
            children=rows
        )
