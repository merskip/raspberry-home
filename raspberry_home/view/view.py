from abc import ABC, abstractmethod

from raspberry_home.controller.view.geometry import *
from raspberry_home.view.render import RenderContext


class View(ABC):

    is_show_bounds = False

    @staticmethod
    def set_show_bounds(is_show_bounds: bool):
        View.is_show_bounds = is_show_bounds

    @abstractmethod
    def content_size(self, container_size: Size) -> Size:
        pass

    @abstractmethod
    def render(self, context: RenderContext):
        pass

    def render_bounds(self, context: RenderContext, frame: Rect = None, color=(0, 127, 255, 127)):
        if View.is_show_bounds:
            if frame is None:
                frame = Rect(origin=context.origin, size=self.content_size(context.container_size))
            context.draw.rectangle(
                xy=frame.adding(width=-1, height=-1).xy,
                outline=color
            )
