import unittest

from raspberry_home.view.center import Center
from raspberry_home.view.geometry import Point
from raspberry_home.view.padding import Padding, Size, EdgeInsets
from tests.MagicView import MagicView


class TestCenter(unittest.TestCase):

    def test_center(self):
        center = Center(
            child=MagicView(
                content_size=Size(100, 100),
                expected_container_size=Size(200, 200),
                expected_origin=Point(50, 50),
            )
        )
        MagicView.test_render(
            root_view=center,
            container_size=Size(200, 200),
            expected_content_size=Size(100, 100),
        )


if __name__ == '__main__':
    unittest.main()
