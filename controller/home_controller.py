from PIL import ImageFont, Image, ImageDraw, ImageColor

from display.display import Display
from platform.platform import Platform

EPD_WIDTH = 176
EPD_HEIGHT = 264


class HomeController:

    font = ImageFont.truetype("fonts/Ubuntu-Medium.ttf", 15)

    def __init__(self, platform: Platform, display: Display):
        self.platform = platform
        self.display = display

    def refresh(self):
        image_black = Image.new('1', self.display.get_size(), 255)
        image_red = Image.new('1', self.display.get_size(), 255)
        draw_black = ImageDraw.Draw(image_black)
        draw_red = ImageDraw.Draw(image_red)

        text = ""
        for sensor in self.platform.get_sensors():
            values = ",\n ".join(list(map(lambda c: sensor.get_value_with_unit(c), sensor.get_characteristics())))
            text += "%s: %s\n" % (sensor.name, values)

        draw_black.rectangle([(0, 0), self.display.get_size()], fill=ImageColor.colormap["black"])
        draw_black.multiline_text((16, 16), text, font=self.font, fill=ImageColor.colormap["white"])

        self.display.draw(image_black, image_red)
