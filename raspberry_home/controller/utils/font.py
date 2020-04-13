import os
from enum import Enum

from PIL import ImageFont

from raspberry_home.assets import Assets


class FontWight(Enum):
    REGULAR = 'Regular'
    MEDIUM = 'Medium'
    BOLD = 'Bold'


class Font:

    def __init__(self, size: int, weight: FontWight = FontWight.REGULAR):
        self.size = size
        self.weight = weight

    def load(self):
        return ImageFont.truetype(self.get_path(), self.size)

    def get_path(self):
        return {
            FontWight.REGULAR: Assets.Fonts.ubuntu_regular,
            FontWight.MEDIUM: Assets.Fonts.ubuntu_medium,
            FontWight.BOLD: Assets.Fonts.ubuntu_bold,
        }[self.weight]

    @staticmethod
    def get_default():
        return Font(15, FontWight.MEDIUM)
