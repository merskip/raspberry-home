import os
from enum import Enum

from PIL import ImageFont

from raspberry_home.assets import Assets


class FontWeight(Enum):
    REGULAR = 'Regular'
    MEDIUM = 'Medium'
    BOLD = 'Bold'


class Font:

    def __init__(self, size: int, weight: FontWeight = FontWeight.REGULAR):
        self.size = size
        self.weight = weight

    def load(self):
        return ImageFont.truetype(self.get_path(), self.size)

    def get_path(self):
        return {
            FontWeight.REGULAR: Assets.Fonts.ubuntu_regular,
            FontWeight.MEDIUM: Assets.Fonts.ubuntu_medium,
            FontWeight.BOLD: Assets.Fonts.ubuntu_bold,
        }[self.weight]

    @staticmethod
    def get_default():
        return Font(15, FontWeight.MEDIUM)
