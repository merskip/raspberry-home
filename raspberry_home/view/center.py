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
