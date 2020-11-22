import unittest

from raspberry_home.view.text import Text, Size
from tests.MagicView import MagicView


class TestText(unittest.TestCase):

    def setUp(self):
        MagicView.reset()

    def test_render(self):
        text = Text(
            "Hello world!"
        )
        MagicView.test_render(
            root_view=text,
            container_size=Size(200, 200),
            expected_content_size=Size(86, 17)  # Some fixed value
        )


if __name__ == '__main__':
    unittest.main()
