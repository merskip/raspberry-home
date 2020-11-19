from raspberry_home.view.color import Color
from raspberry_home.view.render import RenderContext
from raspberry_home.view.view import *


class Padding(View):

    def __init__(self, padding: EdgeInsets, child: View):
        self.padding = padding
        self.child = child

    def content_size(self, container_size: Size) -> Size:
        child_container_size = container_size.adding(
            width=-(self.padding.left + self.padding.right),
            height=-(self.padding.top + self.padding.bottom),
        )
        content_size = self.child.content_size(child_container_size)
        return content_size.adding(
            width=self.padding.left + self.padding.right,
            height=self.padding.top + self.padding.bottom,
        )

    def render(self, context: RenderContext):
        child_origin = context.origin.adding(self.padding.left, self.padding.top)
        child_container_size = context.container_size.adding(
            width=-(self.padding.left + self.padding.right),
            height=-(self.padding.top + self.padding.bottom),
        )
        self.child.render(context.copy(
            origin=child_origin,
            container_size=child_container_size
        ))
        self._render_debug_bounds(context)

    def _render_debug_bounds(self, context: RenderContext):
        # Left
        self.render_view_filled_bounds(
            context,
            frame=Rect(Point(context.origin.x, context.origin.y),
                       Size(self.padding.left, context.container_size.height)),
            color=Color.magnate().copy(alpha=0.1),
        )
        # Top
        self.render_view_filled_bounds(
            context,
            frame=Rect(Point(context.origin.x + self.padding.left, context.origin.y),
                       Size(context.container_size.width, self.padding.top)),
            color=Color.magnate().copy(alpha=0.1),
        )
        # Right
        self.render_view_filled_bounds(
            context,
            frame=Rect(Point(context.origin.x + context.container_size.width - self.padding.right,
                             context.origin.y + self.padding.top),
                       Size(self.padding.right, context.container_size.height - self.padding.top)),
            color=Color.magnate().copy(alpha=0.1),
        )
        # Bottom
        self.render_view_filled_bounds(
            context,
            frame=Rect(Point(context.origin.x + self.padding.left,
                             context.origin.y + context.container_size.height - self.padding.bottom),
                       Size(context.container_size.width - self.padding.left - self.padding.right, self.padding.bottom)),
            color=Color.magnate().copy(alpha=0.1),
        )
