import unittest

from raspberry_home.view.geometry import Point
from raspberry_home.view.padding import Padding, Size, EdgeInsets
from tests.MagicView import MagicView


class TestPadding(unittest.TestCase):

    def test_padding_zero(self):
        padding = Padding(
            padding=EdgeInsets.zero(),
            child=MagicView(
                content_size=Size(100, 100),
                expected_container_size=Size(200, 200),
                expected_origin=Point(0, 0),
            )
        )
        MagicView.test_render(
            root_view=padding,
            container_size=Size(200, 200),
            expected_content_size=Size(100, 100),
        )

    def test_padding_all(self):
        padding = Padding(
            padding=EdgeInsets.all(10),
            child=MagicView(
                content_size=Size(100, 100),
                expected_container_size=Size(180, 180),
                expected_origin=Point(10, 10),
            )
        )
        MagicView.test_render(
            root_view=padding,
            container_size=Size(200, 200),
            expected_content_size=Size(120, 120),
        )

    def test_padding_symmetric(self):
        padding = Padding(
            padding=EdgeInsets.symmetric(horizontal=10, vertical=20),
            child=MagicView(
                content_size=Size(100, 100),
                expected_container_size=Size(180, 160),
                expected_origin=Point(10, 20),
            )
        )
        MagicView.test_render(
            root_view=padding,
            container_size=Size(200, 200),
            expected_content_size=Size(120, 140),
        )

    def test_padding_specific(self):
        padding = Padding(
            padding=EdgeInsets(10, 20, 30, 40),
            child=MagicView(
                content_size=Size(100, 100),
                expected_container_size=Size(160, 140),
                expected_origin=Point(10, 20),
            )
        )
        MagicView.test_render(
            root_view=padding,
            container_size=Size(200, 200),
            expected_content_size=Size(140, 160)
        )


if __name__ == '__main__':
    unittest.main()
