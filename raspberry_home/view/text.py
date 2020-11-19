from enum import Enum

from raspberry_home.view.font import Font
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
            font: Font = Font.default(),
            spacing: int = None,
    ):
        self.text = text
        self.align = align
        self.color = color
        self.font = font.load()
        self.spacing = spacing if spacing is not None else font.size * 0.25

    def content_size(self, container_size: Size) -> Size:
        width = 0
        lines = self.text.splitlines()
        for line in lines:
            line_width, _ = self.font.getsize(line)
            width = max(width, line_width)

        ascent, descent = self.font.getmetrics()
        line_height = ascent + descent
        height = len(lines) * line_height + (len(lines) - 1) * self.spacing

        return Size(width, height)

    def render(self, context: RenderContext):
        ascent, descent = self.font.getmetrics()
        context.draw.multiline_text(
            xy=context.origin.xy,
            text=self.text,
            align=self.align.value,
            fill=self.color.rgba,
            font=self.font,
            spacing=self.spacing
        )
        self._render_debug(context)

    def _render_debug(self, context: RenderContext):
        content_size = self.content_size(context.container_size)
        ascent, descent = self.font.getmetrics()
        Renderable.render_view_bounds(
            context,
            frame=Rect(context.origin, content_size),
            color=Color.blue().copy(alpha=0.5)
        )

        x, y = context.origin.xy
        for _ in self.text.splitlines():
            Renderable.render_view_line(
                context,
                start=Point(x + 1, y + ascent - 1),
                end=Point(x + content_size.width - 2, y + ascent - 1),
                color=Color.blue().copy(alpha=0.3)
            )
            y += ascent + self.spacing
