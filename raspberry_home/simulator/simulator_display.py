from PIL import Image
from PyQt5.QtGui import QImage

from raspberry_home.display.display import Display
from raspberry_home.simulator.simulator_window import SimulatorWindow


class SimulatorDisplay(Display):

    def __init__(self, size: (int, int), simulator_window: SimulatorWindow):
        self.size = size
        self.simulator_window = simulator_window
        self.show(self.create_image())

    def get_size(self) -> (int, int):
        return self.size

    def show(self, image: Image):
        image = self._convert_image(image)
        self.simulator_window.set_display(image)

    def _convert_image(self, image: Image):
        image = image.convert('RGB')
        image_bytes = image.tobytes("raw", "RGB")
        return QImage(image_bytes, self.size[0], self.size[1], QImage.Format_RGB888)
