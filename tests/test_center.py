import unittest

from raspberry_home.view.center import Center
from raspberry_home.view.geometry import Point
from raspberry_home.view.padding import Padding, Size, EdgeInsets
from tests.MockView import MockView


class TestCenter(unittest.TestCase):

    def test_center(self):
        center = Center(
            child=MockView(
                content_size=Size(100, 100),
                check_container_size=lambda size: self.assertEqual(Size(200, 200), size),
                check_origin=lambda origin: self.assertEqual(Point(50, 50), origin),
            )
        )
        MockView.test_render(
            root_view=center,
            container_size=Size(200, 200),
            check_content_size=lambda content_size: self.assertEqual(Size(100, 100), content_size)
        )


if __name__ == '__main__':
    unittest.main()
