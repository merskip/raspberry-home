from enum import Enum

from PIL import ImageFont


class FontWight(Enum):
    REGULAR = 'Regular'
    MEDIUM = 'Medium'
    BOLD = 'Bold'


class Font:

    def __init__(self, size: int, weight: FontWight = FontWight.REGULAR):
        self.size = size
        self.weight = weight

    def load(self):
        return ImageFont.truetype("fonts/Ubuntu-%s.ttf" % self.weight.value, self.size)

    @staticmethod
    def get_default():
        return Font(15, FontWight.MEDIUM)
