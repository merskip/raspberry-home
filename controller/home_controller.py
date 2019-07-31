from datetime import datetime
from typing import Callable

from PIL import ImageFont
from PIL import Image
from PIL.ImageDraw import ImageDraw

from display.display import Display
from platform.platform import Platform
from platform.sensor import Characteristic, Characteristics, Sensor, SpecificType
import time

font = ImageFont.truetype("fonts/Ubuntu-Medium.ttf", 15)
titleFont = ImageFont.truetype("fonts/Ubuntu-Bold.ttf", 18)


class HomeController:

    def __init__(self, platform: Platform, display: Display):
        self.platform = platform
        self.display = display

    def begin_refreshing(self):
        import schedule
        schedule.every(5).minutes.do(self.refresh)
        self.refresh()

        while 1:
            schedule.run_pending()
            time.sleep(1)

    def refresh(self):
        (black_image, red_image) = self.display.new_image_draw()

        current_time = datetime.now()
        header = current_time.strftime("%H:%M")
        header_size_width, header_size_height = titleFont.getsize(header)
        black_image.rectangle((0, 0, (header_size_width + 16, header_size_height + 16)), fill=0)
        black_image.text((8, 8), header, font=titleFont, fill=255)
        red_image.text((8 + header_size_width + 16, 8), current_time.strftime("%a, %d.%m"), font=titleFont)

        top_margin = header_size_height + 16 + 12
        display_width, display_height = self.display.get_size()
        grid_layout = GridLayout(origin=(0, top_margin),
                                 size=(display_width, display_height - top_margin),
                                 columns=3, rows=2)

        for sensor in self.platform.get_sensors():
            primary_characteristic = sensor.get_characteristics()[0]

            value = sensor.get_value(primary_characteristic)
            icon = self._get_icon(primary_characteristic, value)
            title = self._get_title(sensor, primary_characteristic, value)

            grid_layout.add_item(GridLayout.Item(icon, title))

        def _draw_item(item: GridLayout.Item, x: int, y: int, cell_width: int, cell_height: int):
            black_image.bitmap((x + (cell_width - item.icon.width) / 2, y), item.icon)

            text_width, text_height = font.getsize(item.text)
            black_image.text((x + (cell_width - text_width) / 2, y + item.icon.height + 4), item.text, font=font)

        grid_layout.draw(_draw_item)

        self.display.draw()

    @staticmethod
    def _get_icon(characteristic: Characteristic, value):
        if characteristic == Characteristics.temperature:
            if characteristic.specific_type == SpecificType.temperature_outside:
                return "assets/ic-temperature-outside.bmp"
            else:
                return "assets/ic-temperature.bmp"
        elif characteristic == Characteristics.light:
            return "assets/ic-day-and-night.bmp"
        elif characteristic == Characteristics.pressure:
            return "assets/ic-pressure-gauge.bmp"
        elif characteristic == Characteristics.boolean:
            if characteristic.specific_type == SpecificType.boolean_door:
                return "assets/ic-door-closed.bmp" if value else "assets/ic-door-open.bmp"
            else:
                return "assets/ic-boolean-true.bmp" if value else "assets/ic-boolean-false.bmp"
        elif characteristic == Characteristics.humidity:
            return "assets/ic-humidity.bmp"
        else:
            raise ValueError("Unknown characteristic: " + characteristic.name)

    @staticmethod
    def _get_title(sensor: Sensor, characteristic: Characteristic, value):
        if characteristic == Characteristics.boolean and characteristic.specific_type == SpecificType.boolean_door:
            return sensor.name
        else:
            return Sensor.format_value_with_unit(characteristic, value)


class GridLayout:
    class Item:
        def __init__(self, image_filename: str, text: str):
            self.icon = Image.open(image_filename).convert("1")
            self.text = text

    def __init__(self, origin: (int, int), size: (int, int), columns: int, rows: int):
        self.origin = origin
        self.size = size
        self.columns = columns
        self.rows = rows
        self.items = []

    def add_item(self, item: Item):
        if len(self.items) >= self.columns * self.rows:
            raise ValueError("Max items reached")
        self.items.append(item)

    def draw(self, callback: Callable[[Item, int, int, int, int], None]):
        column, row = 0, 0
        column_width = self.size[0] / self.columns
        row_height = self.size[1] / self.rows

        for item in self.items:
            x = self.origin[0] + column * column_width
            y = self.origin[1] + row * row_height

            callback(item, x, y, column_width, row_height)

            column += 1
            if column >= self.columns:
                column = 0
                row += 1
