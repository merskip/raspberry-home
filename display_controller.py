from PIL import ImageFont, Image, ImageDraw

from display.display import Display
from platform.platform import Platform

EPD_WIDTH = 176
EPD_HEIGHT = 264


class DisplayController:

    font = ImageFont.truetype("fonts/Ubuntu-Medium.ttf", 15)

    def __init__(self, platform: Platform, display: Display):
        self.platform = platform
        self.display = display

    def refresh(self):
        image_black = Image.new('1', (EPD_HEIGHT, EPD_WIDTH), 255)
        image_red = Image.new('1', (EPD_HEIGHT, EPD_WIDTH), 255)
        draw_black = ImageDraw.Draw(image_black)
        raw_red = ImageDraw.Draw(image_red)

        text = ""
        for sensor in self.platform.get_sensors():
            values = ", ".join(list(map(lambda c: sensor.get_value_with_unit(c), sensor.get_characteristics())))
            text += "%s: %s\n" % (sensor.name, values)

        draw_black.multiline_text((16, 56), text, font=self.font)

        self.display.draw(image_black, image_red)
