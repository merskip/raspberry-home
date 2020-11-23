from raspberry_home.view.geometry import Size
from raspberry_home.view.render import RenderContext
from raspberry_home.view.view import View


class EmptyView(View):

    def content_size(self, container_size: Size) -> Size:
        return Size.zero()

    def render(self, context: RenderContext):
        pass
