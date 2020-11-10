from raspberry_home.controller.utils.font import Font
from raspberry_home.view.view import *


class Text(View):

    def __init__(self, text: str, font: Font = Font.get_default()):
        self.text = text
        self.font = font

    def content_size(self, container_size: Size) -> Size:
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