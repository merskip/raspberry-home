import unittest

from raspberry_home.view.geometry import Point
from raspberry_home.view.padding import Padding, Size, EdgeInsets
from tests.MockView import MockView


class TestPadding(unittest.TestCase):

    def test_padding_zero(self):
        padding = Padding(
            padding=EdgeInsets.zero(),
            child=MockView(
                content_size=Size(100, 100),
                check_container_size=lambda size: self.assertEqual(Size(200, 200), size),
                check_origin=lambda origin: self.assertEqual(Point(0, 0), origin),
            )
        )
        MockView.test_render(
            root_view=padding,
            container_size=Size(200, 200),
            check_content_size=lambda content_size: self.assertEqual(Size(100, 100), content_size)
        )

    def test_padding_all(self):
        padding = Padding(
            padding=EdgeInsets.all(10),
            child=MockView(
                content_size=Size(100, 100),
                check_container_size=lambda size: self.assertEqual(Size(180, 180), size),
                check_origin=lambda origin: self.assertEqual(Point(10, 10), origin),
            )
        )
        MockView.test_render(
            root_view=padding,
            container_size=Size(200, 200),
            check_content_size=lambda content_size: self.assertEqual(Size(120, 120), content_size)
        )

    def test_padding_symmetric(self):
        padding = Padding(
            padding=EdgeInsets.symmetric(horizontal=10, vertical=20),
            child=MockView(
                content_size=Size(100, 100),
                check_container_size=lambda size: self.assertEqual(Size(180, 160), size),
                check_origin=lambda origin: self.assertEqual(Point(10, 20), origin),
            )
        )
        MockView.test_render(
            root_view=padding,
            container_size=Size(200, 200),
            check_content_size=lambda content_size: self.assertEqual(Size(120, 140), content_size)
        )

    def test_padding_specific(self):
        padding = Padding(
            padding=EdgeInsets(10, 20, 30, 40),
            child=MockView(
                content_size=Size(100, 100),
                check_container_size=lambda size: self.assertEqual(Size(160, 140), size),
                check_origin=lambda origin: self.assertEqual(Point(10, 20), origin),
            )
        )
        MockView.test_render(
            root_view=padding,
            container_size=Size(200, 200),
            check_content_size=lambda content_size: self.assertEqual(Size(140, 160), content_size)
        )


if __name__ == '__main__':
    unittest.main()
