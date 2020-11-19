from raspberry_home.view.color import Color
from raspberry_home.view.render import RenderContext
from raspberry_home.view.view import *


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
        self._render_debug_lines(context, content_size)

    def _render_debug_lines(self, context: RenderContext, content_size: Size):
        self.render_view_line(
            context,
            start=Point(
                x=context.origin.x,
                y=context.origin.y + context.container_size.height // 2,
            ),
            end=Point(
                x=context.origin.x + (context.container_size.width - content_size.width) // 2 - 1,
                y=context.origin.y + context.container_size.height // 2,
            ),
            color=Color.magnate().copy(alpha=0.4)
        )

        self.render_view_line(
            context,
            start=Point(
                x=context.origin.x + context.container_size.width // 2,
                y=context.origin.y,
            ),
            end=Point(
                x=context.origin.x + context.container_size.width // 2,
                y=context.origin.y + (context.container_size.height - content_size.height) // 2,
            ),
            color=Color.magnate().copy(alpha=0.4)
        )

        self.render_view_line(
            context,
            start=Point(
                x=context.origin.x + (content_size.width + context.container_size.width) // 2,
                y=context.origin.y + context.container_size.height // 2,
            ),
            end=Point(
                x=context.origin.x + context.container_size.width - 1,
                y=context.origin.y + context.container_size.height // 2,
            ),
            color=Color.magnate().copy(alpha=0.4)
        )

        self.render_view_line(
            context,
            start=Point(
                x=context.origin.x + context.container_size.width // 2,
                y=context.origin.y + (content_size.height + context.container_size.height) // 2
            ),
            end=Point(
                x=context.origin.x + context.container_size.width // 2,
                y=context.origin.y + context.container_size.height,
            ),
            color=Color.magnate().copy(alpha=0.4)
        )
