from PIL import ImageOps

from raspberry_home.view.view import *
import PIL.Image as PILImage


class Image(View):

    def __init__(self, filename: str, invert: bool = True):
        self.filename = filename
        self.invert = invert

    def render(self, context: RenderContext):
        image = PILImage.open(self.filename)
        if self.invert:
            image = ImageOps.invert(image).convert('1')
        else:
            image = image.convert('1')
        context.draw.bitmap(
            context.origin,
            image,
            fill=0
        )
        self.render_bounds(context)