from PIL.ImageQt import ImageQt
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter, QPaintEvent
from PyQt5.QtWidgets import QMainWindow

from raspberry_home.view.render import FixedSizeRender, ColorSpace
from raspberry_home.view.view import View, Size


class TestWindow(QMainWindow):

    def __init__(self, root_view: View):
        self.root_view = root_view
        super(TestWindow, self).__init__()
        min_size = root_view.content_size(Size.zero())
        self.setMinimumSize(min_size.width, min_size.height)

    def paintEvent(self, a0: QPaintEvent) -> None:
        painter = QPainter(self)
        size = self.size()
        render = FixedSizeRender(
            size=Size(size.width(), size.height()),
            color_space=ColorSpace.RGB
        )
        image = render.render(self.root_view)
        painter.drawImage(QPoint(0, 0), ImageQt(image))
