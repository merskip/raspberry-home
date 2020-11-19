from typing import Callable

import PIL.Image as PILImage
from PIL.ImageDraw import ImageDraw

from raspberry_home.view.color import Color
from raspberry_home.view.geometry import Size
from raspberry_home.view.render import RenderContext, ColorSpace
from raspberry_home.view.view import View, Point


class MockView(View):

    def __init__(
            self,
            content_size: Size,
            check_container_size: Callable[[Size], None] = None,
            check_origin: Callable[[Point], None] = None
    ):
        self._content_size = content_size
        self.check_container_size = check_container_size
        self.check_origin = check_origin

    def content_size(self, container_size: Size) -> Size:
        if self.check_container_size is not None:
            self.check_container_size(container_size)
        return self._content_size

    def render(self, context: RenderContext):
        if self.check_container_size is not None:
            self.check_container_size(context.container_size)
        if self.check_origin is not None:
            self.check_origin(context.origin)

    @staticmethod
    def test_render(root_view: View, container_size: Size, check_content_size: Callable[[Size], None]):
        context = RenderContext(
            origin=Point.zero(),
            container_size=container_size,
            draw=ImageDraw(PILImage.new(ColorSpace.RGB.value, container_size.xy, Color.clear().rgba)),
            color_space=ColorSpace.RGB
        )
        content_size = root_view.content_size(container_size)
        check_content_size(content_size)
        root_view.render(context)

