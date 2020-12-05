from PIL import ImageDraw
from raspberry_home.controller.view.view import _Label

from raspberry_home.controller.home_controller import Fonts
from raspberry_home.controller.input_controller import NavigationItem
from raspberry_home.display.display import Display


class ChartController(NavigationItem):

    def __init__(self, display: Display):
        self.display = display

    def selected_show(self):
        image = self.display.create_image()
        image_draw = ImageDraw.Draw(image)

        width, height = self.display.get_size()
        label = _Label("ChartController", Fonts.valueFont) \
            .centered(in_width=width, in_height=height)
        label.draw(image_draw)

        self.display._show(image)
