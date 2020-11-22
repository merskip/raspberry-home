from abc import ABC, abstractmethod

from PIL import Image

from raspberry_home.view.view import View


class Display(ABC):

    def __init__(self):
        self.root_view = None

    def create_image(self):
        return Image.new('RGB', self.get_size(), (255, 255, 255))

    @abstractmethod
    def get_size(self) -> (int, int):
        pass

    def set_view(self, root_view: View):
        self.root_view = root_view
        self._show(root_view)

    def refresh(self):
        if self.root_view is not None:
            self._show(self.root_view)

    @abstractmethod
    def _show(self, root_view: View):
        pass
