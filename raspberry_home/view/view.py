from abc import ABC, abstractmethod
from typing import Tuple

from raspberry_home.controller.view.geometry import *
from raspberry_home.view.render import RenderContext


class BoxConstraints:

    def __init__(self, minimum_size: Size, maximum_size: Size):
        self.minimum_size = minimum_size
        self.maximum_size = maximum_size

    @staticmethod
    def fixed(size: Size):
        return BoxConstraints(size, size)


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

    def render_bounds(
            self,
            context: RenderContext,
            frame: Rect = None,
            color: Tuple[int, int, int, int] = (0, 127, 255, 127),
            width: int = 1,
            fill=False
    ):
        if View.is_show_bounds:
            if frame is None:
                frame = Rect(origin=context.origin, size=self.content_size(context.container_size))
            frame = frame.adding(width=-1, height=-1)

            if fill:
                context.draw.rectangle(
                    xy=frame.xy,
                    fill=color
                )
            else:
                # Draw edges: top, right, bottom, left
                context.draw.rectangle(
                    xy=Rect(
                        origin=frame.origin,
                        size=Size(frame.size.width, height=width - 1)
                    ).xy,
                    fill=color, width=width
                )
                context.draw.rectangle(
                    xy=Rect(
                        origin=Point(x=frame.max_x - width + 1, y=frame.min_y + width),
                        size=Size(width - 1, height=frame.size.height - width)
                    ).xy,
                    fill=color, width=width
                )
                context.draw.rectangle(
                    xy=Rect(
                        origin=Point(x=frame.min_x, y=frame.max_y - width + 1),
                        size=Size(frame.size.width - width, height=width - 1)
                    ).xy,
                    fill=color, width=width
                )
                context.draw.rectangle(
                    xy=Rect(
                        origin=Point(x=frame.min_x, y=frame.min_y + width),
                        size=Size(width - 1, height=frame.size.height - 2 * width)
                    ).xy,
                    fill=color, width=width
                )