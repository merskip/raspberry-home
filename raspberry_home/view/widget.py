from abc import ABC, abstractmethod

from raspberry_home.view.render import RenderContext
from raspberry_home.view.view import View, Size


class Widget(View, ABC):

    def content_size(self, container_size: Size) -> Size:
        return self.build().content_size(container_size)

    def render(self, context: RenderContext):
        self.build().render(context)

    @abstractmethod
    def build(self) -> View:
        pass
