from PIL import Image

from display.display import Display


class SaveFileDisplay(Display):

    def __init__(self, filename: str, size: (int, int)):
        self._filename = filename
        self._size = size

    def get_size(self) -> (int, int):
        return self._size

    def draw(self):
        width, height = self.get_size()

        result_image = Image.new('RGB', self.get_size(), 255)
        result_image.paste(self.black_image)

        # Draw red image on black image as result image
        result_image_pixels = result_image.load()
        red_image_pixels = self.red_image.load()
        for x in range(width):
            for y in range(height):
                if red_image_pixels[x, y] == 0:
                    result_image_pixels[x, y] = (255, 0, 0)

        result_image.save(self._filename)
