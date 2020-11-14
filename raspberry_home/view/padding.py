from raspberry_home.view.view import *


class Padding(View):

    def __init__(self, padding: int, child: View):
        self.padding = padding
        self.child = child

    def content_size(self, container_size: Size) -> Size:
        child_container_size = container_size.adding(
            width=self.padding * -2,
            height=self.padding * -2,
        )
        content_size = self.child.content_size(child_container_size)
        return content_size.adding(
            width=self.padding * 2,
            height=self.padding * 2
        )

    def render(self, context: RenderContext):
        child_origin = context.origin.adding(self.padding, self.padding)
        child_container_size = context.container_size.adding(
            width=self.padding * -2,
            height=self.padding * -2,
        )
        self.child.render(context.copy(
            origin=child_origin,
            container_size=child_container_size
        ))
        child_content_size = self.child.content_size(child_container_size)
        self.render_bounds(
            context,
            frame=Rect(context.origin, child_content_size.adding(width=self.padding * 2, height=self.padding * 2)),
            color=(255, 0, 127, 32),
            width=self.padding
        )
