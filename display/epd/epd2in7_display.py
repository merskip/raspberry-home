from display.display import Display
from display.epd.epd2in7_driver import EPD2in7Driver
from display.epd.epd_hardware import EPDHardware
from display.epd.epd_lut import EPD2in7DefaultLUTSet


class EPD2in7Display(Display):

    def __init__(self):
        epd_hardware = EPDHardware(spi_bus=0, spi_device=0,
                                   reset_pin=17, dc_pin=25, cs_pin=8, busy_pin=24)
        self._driver = EPD2in7Driver(epd_hardware)

    def get_size(self) -> (int, int):
        return self._driver.width, self._driver.height

    def draw(self):
        self._driver.init_sequence(EPD2in7DefaultLUTSet())
        self._driver.display(self.black_image, self.red_image)
        self._driver.deep_sleep()
