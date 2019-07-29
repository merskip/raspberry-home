from PIL import Image, ImageDraw
from display.display import Display
from epd import epd2in7b


class EPD2in7BDisplay(Display):

    def __init__(self):
        self.epd = epd2in7b.EPD()
        self.epd.init()

    def draw(self, black_image: Image, red_image: Image):
        black_buffer = self.epd.getbuffer(black_image)
        red_buffer = self.epd.getbuffer(red_image)

        self.epd.display(black_buffer, red_buffer)
        self.epd.sleep()
