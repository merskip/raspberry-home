from datetime import datetime
from typing import Callable, List

from PIL import Image as PILImage, ImageDraw, ImageOps
from PIL import ImageFont

from controller.font import Font, FontWight
from controller.moon import MoonPhase, Moon
from controller.sun import Sun
from controller.view.geometry import Size
from controller.view.view import Label, Image
from display.display import Display
from platform.characteristic import Characteristic, Characteristics
from platform.measurement import Measurement
from platform.measurements_scheduler import MeasurementsListener
from platform.sensor import Sensor
from sensor.covid19monitor import COVID19Monitor


class Fonts:
    timeFont = Font(32, FontWight.BOLD)
    dateFont = Font(18, FontWight.MEDIUM)
    valueFont = Font(15, FontWight.MEDIUM)


class HomeController(MeasurementsListener):

    def __init__(self, display: Display, coordinates, timezone_offset):
        self.display = display
        self.coordinates = coordinates
        self.timezone_offset = timezone_offset

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
        sunrise_icon = Image("assets/sunrise.png")
        sunrise_icon.set_origin(x=moon_image.get_frame().max_x + 8,
                                y=moon_image.get_frame().min_y - 2)
        sunrise_icon.draw(image_draw)

        sunrise_time = self.time_to_text(sun.calcSunTime(coords=self.coordinates, isRiseTime=True))
        sunrise_label = Label(sunrise_time, font=Font(12, FontWight.MEDIUM))
        sunrise_label.set_origin(x=sunrise_icon.get_frame().max_x + 2,
                                 y=sunrise_icon.get_frame().min_y - 1)
        sunrise_label.draw(image_draw)

        # Sun set
        sunset_icon = Image("assets/sunset.png")
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
            MoonPhase.NEW_MOON: "assets/moon-new-moon.png",
            MoonPhase.WAXING_CRESCENT: "assets/moon-waxing-crescent.png",
            MoonPhase.FIRST_QUARTER: "assets/moon-first-quarter.png",
            MoonPhase.WAXING_GIBBOUS: "assets/moon-waxing-gibbous.png",
            MoonPhase.FULL_MOON: "assets/moon-full-moon.png",
            MoonPhase.WANING_GIBBOUS: "assets/moon-waning-gibbous.png",
            MoonPhase.LAST_QUARTER: "assets/moon-last-quarter.png",
            MoonPhase.WANING_CRESCENT: "assets/moon-waning-crescent.png",
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
        if "\n" in title:
            title_label.set_origin(x=16)
        title_label.draw(image_draw)

    @staticmethod
    def _get_icon(sensor: Sensor, characteristic: Characteristic, value):
        if characteristic == Characteristics.temperature:
            if sensor.has_flag("outside"):
                return "assets/ic-temperature-outside.bmp"
            else:
                return "assets/ic-temperature.bmp"
        elif characteristic == Characteristics.light:
            return "assets/ic-day-and-night.bmp"
        elif characteristic == Characteristics.pressure:
            return "assets/ic-pressure-gauge.bmp"
        elif characteristic == Characteristics.boolean:
            if sensor.has_flag("door"):
                return "assets/ic-door-closed.bmp" if value else "assets/ic-door-open.bmp"
            else:
                return "assets/ic-boolean-true.bmp" if value else "assets/ic-boolean-false.bmp"
        elif characteristic == Characteristics.humidity:
            return "assets/ic-humidity.bmp"
        elif characteristic == Characteristics.virusCases:
            return "assets/ic-virus.bmp"
        elif characteristic == Characteristics.soilMoisture:
            return "assets/ic-flower.bmp"
        else:
            raise ValueError("Unknown characteristic: " + characteristic.name)

    @staticmethod
    def _get_title(sensor: Sensor, characteristic: Characteristic, value):
        if characteristic == Characteristics.boolean and sensor.has_flag("door"):
            return sensor.name
        if characteristic.name == "pressure":
            return str(round(value)) + " " + characteristic.unit
        elif isinstance(sensor, COVID19Monitor):
            return str(value[0]) + "\n" + str(value[1]) + "/" + str(value[2])
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

            self.image.paste(cell_image, (x, y))

        # ImageDraw.Draw(self.image) \
        #     .rectangle([x, y, x + self._column_width - 1, y + self._row_height - 1], outline=0)

        self._current_column += 1
        if self._current_column >= self.columns:
            self._current_column = 0
            self._current_row += 1
