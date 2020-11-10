from raspberry_home.view.view import *


class Padding(View):

    def __init__(self, padding: int, child: View):
        self.padding = padding
        self.child = child

    def content_size(self, container_size: Size) -> Size:
        content_size = self.child.content_size(container_size.adding())
        return content_size.adding(width=self.padding * 2, height=self.padding * 2)

    def render(self, context: RenderContext):
        self.child.render(context.copy(
            origin=Point(x=self.padding, y=self.padding),
            container_size=context.container_size.adding(width=-self.padding, height=-self.padding)
        ))
