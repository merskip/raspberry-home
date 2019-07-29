from abc import ABC, abstractmethod
from PIL import Image


class Display(ABC):

    @abstractmethod
    def draw(self, black_image: Image, red_image: Image):
        pass
