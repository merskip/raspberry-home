from datetime import datetime
from typing import Callable, List

from PIL import Image as PILImage, ImageDraw

from raspberry_home.assets import Assets
from raspberry_home.controller.input_controller import NavigationItem
from raspberry_home.controller.utils.font import Font, FontWight
from raspberry_home.controller.utils.moon import MoonPhase, Moon
from raspberry_home.controller.utils.sun import Sun
from raspberry_home.controller.view.geometry import Size, Rect
from raspberry_home.controller.view.view import Label, Image
from raspberry_home.display.display import Display
from raspberry_home.platform.characteristic import Characteristic, Characteristics
from raspberry_home.platform.measurement import Measurement
from raspberry_home.platform.measurements_scheduler import MeasurementsListener
from raspberry_home.platform.sensor import Sensor
from raspberry_home.sensor.covid19monitor import COVID19Monitor


class Fonts:
    timeFont = Font(32, FontWight.BOLD)
    dateFont = Font(18, FontWight.MEDIUM)
    valueFont = Font(15, FontWight.MEDIUM)


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
        image = self.display.create_image()

        grid_layout = GridLayout(image=image,
                                 rect=((0, 0), self.display.get_size()),
                                 columns=3, rows=2)

        grid_layout.next_cell(self._draw_time_cell)

        grid_layout.next_cell(
            lambda cell_draw, cell_size: self._draw_measurement_cell(measurements[0], cell_draw, cell_size,
                                                                     measurements[1])
        )
        for measurement in measurements[2:]:
            is_primary_characteristic = measurement.sensor.get_characteristics()[0] == measurement.characteristic
            if not is_primary_characteristic:
                continue
            grid_layout.next_cell(
                lambda cell_draw, cell_size: self._draw_measurement_cell(measurement, cell_draw, cell_size)
            )

        self.display.show(image)

    def _draw_time_cell(self, image_draw: ImageDraw, cell_size: Size):
        now = datetime.now()

        time = now.strftime("%H:%M")
        time_label = Label(time, Fonts.timeFont).centered(in_width=cell_size.width)
        time_label.draw(image_draw)

        date = now.strftime("%d.%m")
        date_label = Label(date, Fonts.dateFont).centered(in_width=cell_size.width)
        date_label.layout_bottom(time_label, margin=2)
        date_label.draw(image_draw)

        moon_image = Image(self._get_moon_phase_filename())
        moon_image.set_origin(x=4, y=cell_size.height - moon_image.get_content_size().height - 4)
        moon_image.draw(image_draw)

        sun = Sun()

        # Sun rise
        sunrise_icon = Image(Assets.Images.sunrise)
        sunrise_icon.set_origin(x=moon_image.get_frame().max_x + 8,
                                y=moon_image.get_frame().min_y - 2)
        sunrise_icon.draw(image_draw)

        sunrise_time = self.time_to_text(sun.calcSunTime(coords=self.coordinates, isRiseTime=True))
        sunrise_label = Label(sunrise_time, font=Font(12, FontWight.MEDIUM))
        sunrise_label.set_origin(x=sunrise_icon.get_frame().max_x + 2,
                                 y=sunrise_icon.get_frame().min_y - 1)
        sunrise_label.draw(image_draw)

        # Sun set
        sunset_icon = Image(Assets.Images.sunset)
        sunset_icon.set_origin(x=sunrise_icon.get_frame().min_x,
                               y=sunrise_icon.get_frame().max_y + 2)
        sunset_icon.draw(image_draw)

        sunset_time = self.time_to_text(sun.calcSunTime(coords=self.coordinates, isRiseTime=False))
        sunset_label = Label(sunset_time, font=Font(12, FontWight.MEDIUM))
        sunset_label.set_origin(x=sunrise_label.get_frame().min_x,
                                y=sunset_icon.get_frame().min_y - 1)
        sunset_label.draw(image_draw)

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

    def _draw_measurement_cell(self, measurement: Measurement, image_draw: ImageDraw, cell_size: Size,
                               second_measurement=None):
        sensor = measurement.sensor
        characteristic = measurement.characteristic
        value = measurement.value

        icon_filename = self._get_icon(sensor, characteristic, value)
        icon_image = Image(icon_filename, invert=False).centered(in_width=cell_size.width)
        icon_image.set_origin(y=8)
        icon_image.draw(image_draw)

        title = self._get_title(sensor, characteristic, value)
        if second_measurement is not None:  # TODO: Cleanup
            title = title + "\n" + self._get_title(second_measurement.sensor, second_measurement.characteristic,
                                                   second_measurement.value)
        title_label = Label(title, font=Fonts.valueFont).centered(in_width=cell_size.width)
        title_label.set_origin(y=icon_image.get_frame().max_y + 4)
        title_label.draw(image_draw)

    @staticmethod
    def _get_icon(sensor: Sensor, characteristic: Characteristic, value):
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


class GridLayout:

    def __init__(self, image: ImageDraw, rect: ((int, int), (int, int)), columns: int, rows: int):
        self.image = image
        self.rect = rect
        self.columns = columns
        self.rows = rows
        width, height = rect[1]
        self._column_width = width // self.columns
        self._row_height = height // self.rows
        self._current_column = 0
        self._current_row = 0

    def next_cell(self, callback: Callable[[any, Size], None]):
        """
        :param callback: Called for each item with: item, x, y, column width, row height
        """
        origin_x, origin_y = self.rect[0]
        x = origin_x + self._current_column * self._column_width
        y = origin_y + self._current_row * self._row_height

        if callback is not None:
            cell_image = PILImage.new('RGB', (self._column_width, self._column_width), color=(255, 255, 255))
            cell_image_draw = ImageDraw.Draw(cell_image)
            callback(cell_image_draw, Size(self._column_width, self._row_height))
            # cell_image_draw.rectangle(
            #     xy=Rect.zero().adding(width=self._column_width,height=self._row_height).xy,
            #     outline=(0, 0, 64)
            # )

            self.image.paste(cell_image, (x, y))

        self._current_column += 1
        if self._current_column >= self.columns:
            self._current_column = 0
            self._current_row += 1
