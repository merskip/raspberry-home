import unittest

from raspberry_home.view.text import Text, Size
from tests.MockView import MockView


class TestText(unittest.TestCase):

    def test_render(self):
        text = Text(
            "Hello world!"
        )
        MockView.test_render(
            root_view=text,
            container_size=Size(200, 200),
            check_content_size=lambda content_size: self.assertEqual(Size(86, 17), content_size)
        )


if __name__ == '__main__':
    unittest.main()
