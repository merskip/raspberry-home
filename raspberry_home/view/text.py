from enum import Enum

from raspberry_home.controller.utils.font import Font
from raspberry_home.view.renderable import *
from raspberry_home.view.view import *


class Text(View, Renderable):

    class Align(Enum):
        LEFT = 'left'
        CENTER = 'center'
        RIGHT = 'right'

    def __init__(
            self,
            text: str,
            align: Align = Align.LEFT,
            color: Color = Color.black(),
            font: Font = Font.default()
    ):
        self.text = text
        self.align = align
        self.color = color
        self.font = font
        self.spacing = font.size * 0.25

    def content_size(self, container_size: Size) -> Size:
        width = 0
        font = self.font.load()
        lines = self.text.splitlines()
        for line in lines:
            line_width, _ = font.getsize(line)
            width = max(width, line_width)

        ascent, descent = font.getmetrics()
        line_height = ascent + descent
        height = len(lines) * line_height + (len(lines) - 1) * self.spacing

        return Size(width, height)

    def render(self, context: RenderContext):
        context.draw.multiline_text(
            xy=context.origin.xy,
            text=self.text,
            align=self.align.value,
            fill=self.color.rgba,
            font=self.font.load(),
            spacing=self.spacing
        )
        Renderable.render_view_bounds(
            context,
            frame=Rect(context.origin, self.content_size(context.container_size)),
            color=Color.blue().copy(alpha=0.5)
        )
