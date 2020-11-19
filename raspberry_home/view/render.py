from abc import abstractmethod
from enum import Enum

import PIL.Image as PILImage
from PIL.ImageDraw import ImageDraw

from raspberry_home.view.geometry import Size, Point
from raspberry_home.view.color import Color


class ColorSpace(Enum):
    BINARY = '1'
    RGB = 'RGB'


class RenderContext:

    def __init__(self, origin: Point, container_size: Size, draw: ImageDraw, color_space: ColorSpace):
        self.origin = origin
        self.container_size = container_size
        self.draw = draw
        self.color_space = color_space

    def copy(self, origin: Point = None, container_size: Size = None):
        return RenderContext(
            origin=origin if origin is not None else self.origin,
            container_size=container_size if container_size is not None else self.container_size,
            draw=self.draw,
            color_space=self.color_space
        )


class Render:

    @abstractmethod
    def render(self, root_view):
        pass


class FixedSizeRender(Render):

    def __init__(self, size: Size, color_space: ColorSpace):
        self.size = size
        self.color_space = color_space

    def render(self, root_view) -> PILImage.Image:
        image = PILImage.new(self.color_space.value, self.size.xy, Color.clear().rgba)

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

    def render(self, root_view) -> PILImage.Image:
        content_size = root_view.content_size(Size.zero())
        image = PILImage.new(self.color_space.value, content_size.xy, Color.clear().rgba)

        context = RenderContext(
            origin=Point.zero(),
            container_size=content_size,
            draw=ImageDraw(image, mode=self.color_space.value),
            color_space=self.color_space
        )
        root_view.render(context)
        return image
