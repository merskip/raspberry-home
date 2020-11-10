from raspberry_home.view.view import *


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
