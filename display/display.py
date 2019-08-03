from abc import ABC, abstractmethod

from PIL import Image, ImageDraw


class Display(ABC):
    black_image = None
    red_image = None

    def new_image_draw(self):
        self.black_image = Image.new('1', self.get_size(), 255)
        self.red_image = Image.new('1', self.get_size(), 255)
        return ImageDraw.Draw(self.black_image), ImageDraw.Draw(self.red_image)

    @abstractmethod
    def get_size(self) -> (int, int):
        pass

    @abstractmethod
    def draw(self):
        pass
