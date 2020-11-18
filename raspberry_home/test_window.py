from PIL.ImageQt import ImageQt
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QWindow, QResizeEvent, QImage, QPixmap, QPageLayout, QPainter, QPaintEvent
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QStackedLayout, QGridLayout, QMainWindow

from raspberry_home.view.render import FixedSizeRender, ColorSpace
from raspberry_home.view.view import View, Size


class TestWindow(QMainWindow):

    def __init__(self, root_view: View):
        self.root_view = root_view
        super(TestWindow, self).__init__()

    def paintEvent(self, a0: QPaintEvent) -> None:
        painter = QPainter(self)
        size = self.size()
        render = FixedSizeRender(
            size=Size(size.width(), size.height()),
            color_space=ColorSpace.RGB
        )
        image = render.render(self.root_view)
        painter.drawImage(QPoint(0, 0), ImageQt(image))
