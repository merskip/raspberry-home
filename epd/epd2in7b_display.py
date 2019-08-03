from display.display import Display
from epd import epd2in7b


class EPD2in7BDisplay(Display):

    def get_size(self) -> (int, int):
        return epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH  # Inverted axis

    def __init__(self):
        self.epd = epd2in7b.EPD()

    def draw(self):
        black_buffer = self.epd.getbuffer(self.black_image)
        red_buffer = self.epd.getbuffer(self.red_image)

        self.epd.init()
        self.epd.display(black_buffer, red_buffer)
        self.epd.sleep()
