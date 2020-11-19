import unittest

from raspberry_home.view.color import Color


class ColorTests(unittest.TestCase):

    def test_color_rgba(self):
        c = Color(128, 96, 160, 0.5)
        self.assertEqual((128, 96, 160, 128), c.rgba)

    def test_color_to_hex(self):
        c = Color(128, 96, 160, 0.5)
        self.assertEqual("#8060a080", c.to_hex())

    def test_color_from_hex(self):
        c = Color.from_hex("#8060a080")
        self.assertEqual((128, 96, 160, 128), c.rgba)


if __name__ == '__main__':
    unittest.main()
