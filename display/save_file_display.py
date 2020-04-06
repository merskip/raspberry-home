from PIL import Image

from display.display import Display


class SaveFileDisplay(Display):

    def __init__(self, filename: str, size: (int, int)):
        self._filename = filename
        self._size = size

    def get_size(self) -> (int, int):
        return self._size

    def show(self, image: Image):
        image = image.convert('1')
        image.save(self._filename + ".bmp")
        image.show()
