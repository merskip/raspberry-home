from abc import ABC, abstractmethod

from raspberry_home.view.color import Color
from raspberry_home.view.geometry import Rect, Size, Point
from raspberry_home.view.render import RenderContext


class Renderable(ABC):

    is_show_frames = False

    @staticmethod
    def set_show_frames(is_show_frames: bool):
        Renderable.is_show_frames = is_show_frames

    @abstractmethod
    def render(self, context: RenderContext):
        pass

    @staticmethod
    def render_view_bounds(context: RenderContext, frame: Rect, color: Color, width: int = 1):
        if not Renderable.is_show_frames:
            return

        frame = frame.adding(width=-1, height=-1)
        color = color.rgba
        # Draw top
        context.draw.rectangle(
            xy=Rect(
                origin=frame.origin,
                size=Size(frame.size.width, width - 1)
            ).xy,
            fill=color, width=width
        )
        # Draw right
        context.draw.rectangle(
            xy=Rect(
                origin=Point(frame.max_x - width + 1, frame.min_y + width),
                size=Size(width - 1, frame.size.height - width)
            ).xy,
            fill=color, width=width
        )
        # Draw bottom
        context.draw.rectangle(
            xy=Rect(
                origin=Point(frame.min_x, frame.max_y - width + 1),
                size=Size(frame.size.width - width, width - 1)
            ).xy,
            fill=color, width=width
        )
        # Draw left
        context.draw.rectangle(
            xy=Rect(
                origin=Point(frame.min_x, frame.min_y + width),
                size=Size(width - 1, frame.size.height - 2 * width)
            ).xy,
            fill=color, width=width
        )

    @staticmethod
    def render_view_line(context: RenderContext, start: Point, end: Point, color: Color):
        if not Renderable.is_show_frames:
            return
        context.draw.line((start.xy, end.xy), fill=color.rgba)

    @staticmethod
    def render_view_filled_bounds(context: RenderContext, frame: Rect, color: Color):
        if not Renderable.is_show_frames:
            return
        frame = frame.adding(width=-1, height=-1)
        context.draw.rectangle(xy=frame.xy, fill=color.rgba)
