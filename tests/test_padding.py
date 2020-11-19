import unittest

from raspberry_home.view.geometry import Point
from raspberry_home.view.padding import Padding, Size
from tests.MockView import MockView


class TestPadding(unittest.TestCase):

    def test_padding_zero(self):
        padding = Padding(
            padding=0,
            child=MockView(
                content_size=Size(100, 100),
                check_container_size=lambda size: self.assertEqual(size, Size(200, 200)),
                check_origin=lambda origin: self.assertEqual(origin, Point(0, 0)),
            )
        )
        padding.render(MockView.render_context(Size(200, 200)))

    def test_padding_ten(self):
        padding = Padding(
            padding=10,
            child=MockView(
                content_size=Size(100, 100),
                check_container_size=lambda size: self.assertEqual(size, Size(180, 180)),
                check_origin=lambda origin: self.assertEqual(origin, Point(10, 10)),
            )
        )
        padding.render(MockView.render_context(Size(200, 200)))


if __name__ == '__main__':
    unittest.main()
