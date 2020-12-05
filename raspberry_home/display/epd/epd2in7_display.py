from PIL import Image

from raspberry_home.display.display import Display
from raspberry_home.display.epd.epd2in7_driver import EPD2in7Driver
from raspberry_home.display.epd.epd_hardware import EPDHardware
from raspberry_home.display.epd.epd_lut import EPD2in7DefaultLUTSet
from raspberry_home.view.geometry import Size
from raspberry_home.view.render import FixedSizeRender, ColorSpace
from raspberry_home.view.view import View


class EPD2in7Display(Display):

    def __init__(self):
        epd_hardware = EPDHardware(spi_bus=0, spi_device=0,
                                   reset_pin=17, dc_pin=25, cs_pin=8, busy_pin=24)
        self._driver = EPD2in7Driver(epd_hardware)
        super().__init__()

    def get_size(self) -> (int, int):
        return self._driver.width, self._driver.height

    def _show(self, root_view: View):
        render = FixedSizeRender(size=Size(self._driver.width, self._driver.height),
                                 color_space=ColorSpace.BINARY)
        image = render.render(root_view)
        black_image = image.convert('1')
        red_image = Image.new('1', self.get_size(), 255)

        self._driver.init_sequence(EPD2in7DefaultLUTSet())
        self._driver.display(black_image, red_image)
        self._driver.deep_sleep()
