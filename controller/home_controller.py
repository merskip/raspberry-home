from datetime import datetime
from PIL import ImageFont
from display.display import Display
from platform.platform import Platform

EPD_WIDTH = 176
EPD_HEIGHT = 264


class HomeController:

    font = ImageFont.truetype("fonts/Ubuntu-Medium.ttf", 15)
    titleFont = ImageFont.truetype("fonts/Ubuntu-Bold.ttf", 18)

    def __init__(self, platform: Platform, display: Display):
        self.platform = platform
        self.display = display

    def refresh(self):
        (black_image, red_image) = self.display.new_image_draw()

        text = ""
        for sensor in self.platform.get_sensors():
            values = ", ".join(list(map(lambda c: sensor.get_value_with_unit(c), sensor.get_characteristics())))
            text += "%s:\t %s\n" % (sensor.name, values)

        current_time = datetime.now()
        header = current_time.strftime("%H:%M")
        header_size = self.titleFont.getsize(header)
        black_image.rectangle((0, 0, (header_size[0] + 16, header_size[1] + 16)), fill=0)
        black_image.text((8, 8), header, font=self.titleFont, fill=255)
        red_image.text((8 + header_size[0] + 16, 8), current_time.strftime("%A, %d.%m"), font=self.titleFont)

        black_image.multiline_text((8, header_size[1] + 16 + 8), text, font=self.font)

        self.display.draw()
