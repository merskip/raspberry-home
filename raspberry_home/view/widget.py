from abc import ABC, abstractmethod

from raspberry_home.view.render import RenderContext
from raspberry_home.view.view import View, Size


class Widget(View, ABC):

    view = None

    def content_size(self, container_size: Size) -> Size:
        return self.get_view().content_size(container_size)

    def render(self, context: RenderContext):
        self.get_view().render(context)
        self.view = None

    def get_view(self) -> View:
        if self.view is None:
            self.view = self.build()
        return self.view

    @abstractmethod
    def build(self) -> View:
        pass
