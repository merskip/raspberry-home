from abc import ABC, abstractmethod

from PIL import Image


class Display(ABC):

    def create_image(self):
        return Image.new('RGB', self.get_size(), (255, 255, 255))

    @abstractmethod
    def get_size(self) -> (int, int):
        pass

    @abstractmethod
    def show(self, image: Image):
        pass
