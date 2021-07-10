from typing import Callable
from unittest.case import TestCase
from unittest.mock import MagicMock

import PIL.Image as PILImage
from PIL.ImageDraw import ImageDraw

from raspberry_home.view.color import Color
from raspberry_home.view.geometry import Size
from raspberry_home.view.render import RenderContext, ColorSpace
from raspberry_home.view.view import View, Point


class MagicView(View):
    renders_called = []

    def __init__(
            self,
            content_size: Size,
            expected_container_size: Size = None,
            expected_origin: Point = None
    ):
        self.name = None
        self._content_size = content_size
        self.expected_container_size = expected_container_size
        self.expected_origin = expected_origin
        self.test_case = TestCase()
        self.render_called = MagicMock()
        MagicView.renders_called.append(self.render_called)

    def named(self, name: str):
        self.name = name
        return self

    def content_size(self, container_size: Size) -> Size:
        if self.expected_container_size is not None:
            self.test_case.assertEqual(self.expected_container_size, container_size,
                                       msg=self._msg("Container size while call content size"))
        return self._content_size

    def render(self, context: RenderContext):
        if self.expected_container_size is not None:
            self.test_case.assertEqual(self.expected_container_size, context.container_size,
                                       msg=self._msg("Container size while call render"))
        if self.expected_origin is not None:
            self.test_case.assertEqual(self.expected_origin, context.origin,
                                       msg=self._msg("Origin while call render"))
        self.render_called()

    def _msg(self, msg: str):
        msg += " (in "
        if self.name is not None:
            msg += "name=\"%s\", " % self.name
        msg += "content_size=%s)" % self._content_size
        return msg

    @staticmethod
    def reset():
        MagicView.renders_called = []

    @staticmethod
    def test_render(root_view: View, container_size: Size, expected_content_size: Size = None):
        context = RenderContext(
            origin=Point.zero(),
            container_size=container_size,
            draw=ImageDraw(PILImage.new(ColorSpace.RGB.value, container_size.xy, Color.clear().rgba)),
            color_space=ColorSpace.RGB
        )
        content_size = root_view.content_size(container_size)
        if expected_content_size is not None:
            TestCase().assertEqual(expected_content_size, content_size,
                                   msg="Expected content size equal to %s, but is %s" % (
                                       expected_content_size, content_size))
        root_view.render(context)

        for render_call in MagicView.renders_called:
            render_call.assert_called_once()
