from PIL import Image
from PyQt5.QtGui import QImage

from raspberry_home.display.display import Display
from raspberry_home.simulator.simulator_window import SimulatorWindow
from raspberry_home.view.geometry import Size
from raspberry_home.view.render import FixedSizeRender, ColorSpace
from raspberry_home.view.view import View


class SimulatorDisplay(Display):

    def __init__(self, size: (int, int), simulator_window: SimulatorWindow):
        self.size = size
        self.simulator_window = simulator_window
        super().__init__()

    def get_size(self) -> (int, int):
        return self.size

    def _show(self, root_view: View):
        width, height = self.get_size()
        render = FixedSizeRender(size=Size(width, height),
                                 color_space=self._get_color_space())
        image = render.render(root_view)
        image = self._convert_image(image)
        self.simulator_window.set_display(image)

    def _get_color_space(self):
        if self.simulator_window.rgb_check_box.isChecked():
            return ColorSpace.RGB
        else:
            return ColorSpace.BINARY

    def _convert_image(self, image: Image):
        image = image.convert('RGB')
        image_bytes = image.tobytes("raw", "RGB")
        return QImage(image_bytes, self.size[0], self.size[1], QImage.Format_RGB888)
