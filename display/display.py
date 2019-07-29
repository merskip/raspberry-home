from abc import ABC, abstractmethod
from PIL import Image


class Display(ABC):

    @abstractmethod
    def get_size(self) -> (int, int):
        pass

    @abstractmethod
    def draw(self, black_image: Image, red_image: Image):
        pass
