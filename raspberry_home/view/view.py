from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, List

from PIL import ImageOps
from PIL.ImageDraw import ImageDraw
import PIL.Image as PILImage

from raspberry_home.controller.utils.font import Font
from raspberry_home.controller.view.geometry import Point, Size, Rect


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


class View(ABC):

    is_show_bounds = False

    @staticmethod
    def set_show_bounds(is_show_bounds: bool):
        View.is_show_bounds = is_show_bounds

    @abstractmethod
    def content_size(self, container_size: Size) -> Size:
        pass

    @abstractmethod
    def render(self, context: RenderContext):
        pass

    def render_bounds(self, context: RenderContext, frame: Rect = None, color=(0, 127, 255, 127)):
        if View.is_show_bounds:
            if frame is None:
                frame = Rect(origin=context.origin, size=self.content_size(context.container_size))
            context.draw.rectangle(
                xy=frame.adding(width=-1, height=-1).xy,
                outline=color
            )


class Container(View):

    def __init__(self, child: View, origin: Point = None, size: Point = None):
        self.child = child
        self.origin = origin
        self.size = size

    def content_size(self, container_size: Size) -> Size:
        size = self.size if self.size is not None else self.child.content_size(container_size)
        return size.adding(
            self.origin.x if self.origin is not None else 0,
            self.origin.y if self.origin is not None else 0
        )

    def render(self, context: RenderContext):
        content_size = self.content_size(context.container_size)
        child_context = context.copy(
            origin=context.origin + self.origin,
            container_size=content_size
        )
        self.child.render(child_context)


class Stack(View):

    def __init__(self, children: List[View]):
        self.children = children

    def content_size(self, container_size: Size) -> Size:
        width, height = 0, 0
        for child in self.children:
            content_size = child.content_size(container_size)
            width = max(width, content_size.width)
            height = max(height, content_size.height)
        return Size(width, height)

    def render(self, context: RenderContext):
        for child in self.children:
            child.render(context)


class VerticalStack(View):

    def __init__(self, children: List[View], spacing: float = 0):
        self.children = children
        self.spacing = spacing

    def content_size(self, container_size: Size) -> Optional[Size]:
        width, height = 0, 0
        for child in self.children:
            content_size = child.content_size(container_size)
            width = max(width, content_size.width)
            height += content_size.height
        height += (len(self.children) - 1) * self.spacing
        return Size(width, height)

    def render(self, context: RenderContext):
        x, y = context.origin.xy
        for child in self.children:
            content_size = child.content_size(context.container_size)
            child.render(context.copy(
                origin=Point(x=x, y=y)
            ))
            y += content_size.height + self.spacing


class HorizontalStack(View):

    def __init__(self, children: List[View], spacing: float = 0):
        self.children = children
        self.spacing = spacing

    def content_size(self, container_size: Size) -> Optional[Size]:
        width, height = 0, 0
        for child in self.children:
            content_size = child.content_size(container_size)
            width += content_size.width
            height = max(height, content_size.height)
        width += (len(self.children) - 1) * self.spacing
        return Size(width, height)

    def render(self, context: RenderContext):
        x, y = context.origin.xy
        for child in self.children:
            content_size = child.content_size(context.container_size)
            child.render(context.copy(
                origin=Point(x=x, y=y)
            ))
            x += content_size.width + self.spacing


class Padding(View):

    def __init__(self, padding: int, child: View):
        self.padding = padding
        self.child = child

    def content_size(self, container_size: Size) -> Size:
        content_size = self.child.content_size(container_size.adding())
        return content_size.adding(width=self.padding * 2, height=self.padding * 2)

    def render(self, context: RenderContext):
        self.child.render(context.copy(
            origin=Point(x=self.padding, y=self.padding)
        ))


class Center(View):

    def __init__(self, child: View):
        self.child = child

    def content_size(self, container_size: Size) -> Size:
        return self.child.content_size(container_size)

    def render(self, context: RenderContext):
        content_size = self.child.content_size(context.container_size)
        self.child.render(context.copy(
            origin=Point(
                x=context.origin.x + (context.container_size.width - content_size.width) // 2,
                y=context.origin.y + (context.container_size.height - content_size.height) // 2
            )
        ))


class Text(View):

    def __init__(self, text: str, font: Font = Font.get_default()):
        self.text = text
        self.font = font

    def content_size(self, container_size: Size) -> Optional[Size]:
        width, height = 0, 0
        font = self.font.load()
        for line in self.text.splitlines():
            line_width, line_height = font.getsize(line)
            width = max(width, line_width)
            height += line_height
        return Size(width, height)

    def render(self, context: RenderContext):
        context.draw.multiline_text(
            xy=context.origin.xy,
            text=self.text,
            fill=(0, 0, 0, 255),
            font=self.font.load(),
            align='center',
        )
        self.render_bounds(context)


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
