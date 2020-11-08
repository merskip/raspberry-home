from abc import ABC, abstractmethod

from PIL import ImageOps
from PIL.ImageDraw import ImageDraw
import PIL.Image as PILImage

from raspberry_home.controller.utils.font import Font
from raspberry_home.controller.view.geometry import Point, Size, Rect


class View(ABC):

    def __init__(self):
        self.origin = Point.zero()

    def centered(self, in_width: int = None, in_height: int = None):
        x, y = self.origin.x, self.origin.y
        content_size = self.get_content_size()
        if in_width is not None:
            x = (in_width - content_size.width) // 2
        if in_height is not None:
            y = (in_height - content_size.height) // 2
        self.set_origin(x, y)
        return self

    def layout_bottom(self, view, margin: int = 0):
        self.set_origin(y=view.get_frame().max_y + margin)

    def set_origin(self, x=None, y=None):
        if x is None:
            x = self.origin.x
        if y is None:
            y = self.origin.y
        self.origin = Point(x, y)

    def get_frame(self) -> Rect:
        return Rect(self.origin, self.get_content_size())

    @abstractmethod
    def get_content_size(self) -> Size:
        pass

    @abstractmethod
    def draw(self, draw: ImageDraw):
        pass
        # draw.rectangle(xy=self.get_frame().xy, outline=127)


class Label(View):

    def __init__(self, text: str, font: Font = Font.get_default()):
        super().__init__()
        self.text = text
        self.font = font

    def get_content_size(self) -> Size:
        width, height = 0, 0
        font = self.font.load()
        for line in self.text.splitlines():
            line_width, line_height = font.getsize(line)
            width = max(width, line_width)
            height += line_height
        return Size(width, height)

    def draw(self, draw: ImageDraw):
        draw.multiline_text(xy=self.origin.xy, text=self.text, fill=0, font=self.font.load(), align='center')
        super().draw(draw)


class Image(View):

    def __init__(self, filename: str, invert=True):
        super().__init__()
        image = PILImage.open(filename)
        if invert:
            self._image = ImageOps.invert(image).convert('1')
        else:
            self._image = image.convert('1')

    def get_content_size(self) -> Size:
        return Size(self._image.size[0], self._image.size[1])

    def draw(self, draw: ImageDraw):
        draw.bitmap(self.origin.xy, self._image, fill=0)
        super().draw(draw)
