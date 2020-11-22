from raspberry_home.view.geometry import Size
from raspberry_home.view.render import RenderContext
from raspberry_home.view.view import View, Point


class Offset(View):

    def __init__(self, offset: Point, child: View):
        self.offset = offset
        self.child = child

    def content_size(self, container_size: Size) -> Size:
        return self.child.content_size(container_size)

    def render(self, context: RenderContext):
        self.child.render(context.copy(
            origin=context.origin + self.offset
        ))
