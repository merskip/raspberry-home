from raspberry_home.view.geometry import Size
from raspberry_home.view.render import RenderContext
from raspberry_home.view.view import View


class SizedBox(View):

    def __init__(self, size: Size):
        self._size = size

    def content_size(self, container_size: Size) -> Size:
        return self._size

    def render(self, context: RenderContext):
        pass
