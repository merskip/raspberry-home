import unittest

from raspberry_home.view.offset import Offset
from raspberry_home.view.geometry import Point, Size
from tests.MagicView import MagicView


class TestOffset(unittest.TestCase):

    def setUp(self):
        MagicView.reset()

    def test_center(self):
        MagicView.test_render(
            root_view=Offset(
                offset=Point(10, 10),
                child=MagicView(
                    content_size=Size(100, 100),
                    expected_container_size=Size(200, 200),
                    expected_origin=Point(10, 10),
                )
            ),
            container_size=Size(200, 200),
            expected_content_size=Size(100, 100),
        )


if __name__ == '__main__':
    unittest.main()
