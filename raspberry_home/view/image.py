import PIL.Image as PILImage
from PIL import ImageOps

from raspberry_home.view.color import Color
from raspberry_home.view.render import RenderContext
from raspberry_home.view.view import *


class Image(View, Renderable):

    def __init__(self, filename: str, invert: bool = True, rotation: int = None):
        self.filename = filename
        self.invert = invert
        self.rotation = rotation
        image = PILImage.open(self.filename)
        if self.invert:
            image = ImageOps.invert(image).convert('1')
        else:
            image = image.convert('1')
        if self.rotation is not None:
            image = image.rotate(self.rotation)
        self.image = image

    def content_size(self, container_size: Size) -> Size:
        return Size(self.image.size[0], self.image.size[1])

    def render(self, context: RenderContext):
        context.draw.bitmap(
            context.origin.xy,
            self.image,
            fill=0
        )
        self.render_view_bounds(
            context,
            frame=Rect(context.origin, self.content_size(context.container_size)),
            color=Color.blue().copy(alpha=0.5),
        )
