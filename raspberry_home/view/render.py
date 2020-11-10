from abc import abstractmethod

from PIL.ImageDraw import ImageDraw

from raspberry_home.controller.view.geometry import Size, Point
from raspberry_home.view.view import View, ColorSpace, RenderContext
import PIL.Image as PILImage


class Render:

    @abstractmethod
    def render(self, root_view: View):
        pass


class FixedSizeRender(Render):

    def __init__(self, size: Size, color_space: ColorSpace):
        self.size = size
        self.color_space = color_space

    def render(self, root_view: View) -> PILImage.Image:
        image = PILImage.new(self.color_space.value, self.size.xy, (255, 255, 255, 255))

        context = RenderContext(
            origin=Point.zero(),
            container_size=self.size,
            draw=ImageDraw(image, mode='RGBA'),
            color_space=self.color_space
        )
        root_view.render(context)
        return image


class FlexibleSizeRender(Render):

    def __init__(self, color_space: ColorSpace):
        self.color_space = color_space

    def render(self, root_view: View) -> PILImage.Image:
        content_size = root_view.content_size(Size.zero())
        image = PILImage.new(self.color_space.value, content_size.xy, (255, 255, 255, 255))

        context = RenderContext(
            origin=Point.zero(),
            container_size=content_size,
            draw=ImageDraw(image, mode='RGBA'),
            color_space=self.color_space
        )
        root_view.render(context)
        return image
