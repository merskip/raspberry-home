from datetime import datetime
from typing import List

from raspberry_home.assets import Assets
from raspberry_home.controller.input_controller import NavigationItem
from raspberry_home.controller.utils.moon import MoonPhase, Moon
from raspberry_home.controller.utils.sun import Sun
from raspberry_home.display.display import Display
from raspberry_home.open_weather_api import OpenWeatherApi
from raspberry_home.platform.characteristic import Characteristic, Characteristics
from raspberry_home.platform.measurement import Measurement
from raspberry_home.platform.measurements_scheduler import MeasurementsListener
from raspberry_home.platform.sensor import Sensor
from raspberry_home.sensor.covid19monitor import COVID19Monitor
from raspberry_home.view.GridWidget import GridWidget
from raspberry_home.view.center import Center
from raspberry_home.view.font import Font, FontWeight
from raspberry_home.view.geometry import Point, EdgeInsets
from raspberry_home.view.image import Image
from raspberry_home.view.offset import Offset
from raspberry_home.view.padding import Padding
from raspberry_home.view.stack import HorizontalStack, VerticalStack, StackAlignment
from raspberry_home.view.text import Text
from raspberry_home.view.view import View
from raspberry_home.view.widget import Widget


class Fonts:
    timeFont = Font(32, FontWeight.BOLD)
    dateFont = Font(18, FontWeight.MEDIUM)
    valueFont = Font(15, FontWeight.MEDIUM)
    sunTimeFont = Font(12, FontWeight.MEDIUM)


class HomeController(MeasurementsListener, NavigationItem):

    def __init__(self, display: Display, sun: Sun, moon: Moon, open_weather_api: OpenWeatherApi):
        self.display = display
        self.sun = sun
        self.moon = moon
        self.open_weather_api = open_weather_api

    def selected_show(self):
        self.display.set_view(
            root_view=Center(
                child=Text("Home controller")
            )
        )

    def on_measurements(self, measurements: List[Measurement]):
        self.display_measurements(measurements)

    def display_measurements(self, measurements: List[Measurement]):
        weather = self.open_weather_api.fetch()
        cells = [
            # First Row
            HomeNowCell(
                sun=self.sun,
                moon=self.moon,
            ),
            self._get_measurements_cell([Characteristics.temperature], measurements),
            self._get_measurements_cell([Characteristics.pressure], measurements),
            # Second Row
            self._get_weather_cell(weather),
            self._get_measurements_cell([Characteristics.humidity], measurements),
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
        measurements_of_types = []
        for of_type in of_types:
            measurements_of_types += self._get_measurements(of_type, measurements, only_primary)
        return MeasurementsCell(measurements_of_types) if len(measurements_of_types) > 0 else None

    def _get_weather_cell(self, weather) -> View:
        weather_icon = self._get_weather_icon(weather['weather'][0]['icon'][:2])
        wind_speed = weather['wind']['speed']
        wind_direction = weather['wind']['deg']

        return HomeItemCell(
            icon=HorizontalStack(
                children=[
                    Image(weather_icon),
                    Image(Assets.Images.ic_wind, invert=False, rotation=-wind_direction),
                ]
            ),
            title="%.1f m/s\n%s" % (wind_speed, HomeController._degrees_to_compass(wind_direction)),
        )

    def _get_measurements(
            self,
            of_type: Characteristic,
            measurements: List[Measurement],
            only_primary: bool = True
    ) -> List[Measurement]:
        return list(filter(
            lambda m: m.characteristic.name == of_type.name and (not only_primary or m.is_primary()),
            measurements))

    def _get_weather_icon(self, icon_id) -> str:
        icons = {
            '01': Assets.Images.ic_weather_clear_sky,
            '02': Assets.Images.ic_weather_few_clouds,
            '03': Assets.Images.ic_weather_scattered_clouds,
            '04': Assets.Images.ic_weather_broken_clouds,
            '09': Assets.Images.ic_weather_shower_rain,
            '10': Assets.Images.ic_weather_rain,
            '11': Assets.Images.ic_weather_thunderstorm,
            '13': Assets.Images.ic_weather_snow,
            '50': Assets.Images.ic_weather_mist,
        }
        return icons[icon_id]

    @staticmethod
    def _degrees_to_compass(deg):
        val = int((deg / 22.5) + .5)
        arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
        return arr[(val % 16)]


class HomeNowCell(Widget):

    def __init__(self, sun: Sun, moon: Moon):
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
        return "%2d:%02d" % (time, time % 1.0 * 60)

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

    def __init__(self, measurements: [Measurement], icon_rotation: int = None):
        self.measurements = measurements
        self.icon_rotation = icon_rotation

    def build(self) -> View:
        primary_measurement = self.measurements[0]
        icon = self._get_icon_filename(primary_measurement)
        value_text = "\n".join(map(lambda m: self._get_title(m), self.measurements))
        return Padding(
            padding=EdgeInsets(top=8),
            child=VerticalStack(
                spacing=4,
                alignment=StackAlignment.Center,
                children=[
                    Image(icon, invert=False, rotation=self.icon_rotation),
                    Center(Text(value_text, font=Fonts.valueFont, align=Text.Align.CENTER))
                ]
            )
        )

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


class HomeItemCell(Widget):

    def __init__(self, icon: View, title: str, font: Font = None):
        self.icon = icon
        self.title = title
        self.font = font

    def build(self) -> View:
        font = self.font
        if font is None:
            font = Fonts.valueFont
        return Padding(
            padding=EdgeInsets(top=8),
            child=VerticalStack(
                spacing=4,
                alignment=StackAlignment.Center,
                children=[
                    self.icon,
                    Center(
                        Text(self.title, font=font, align=Text.Align.CENTER)
                    ),
                ]
            )
        )
