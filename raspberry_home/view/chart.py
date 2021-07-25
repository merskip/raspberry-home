from typing import List, Tuple

from raspberry_home.view.color import Color
from raspberry_home.view.geometry import Size, Point
from raspberry_home.view.render import RenderContext
from raspberry_home.view.view import View


class Chart(View):
    def content_size(self, container_size: Size) -> Size:
        return container_size

    def render(self, context: RenderContext):
        pass



class ChartLine(View):

    def __init__(self, points: List[Tuple[float, float]]):
        self.points = points

    def content_size(self, container_size: Size) -> Size:
        return container_size

    def render(self, context: RenderContext):
        line_sequence = []

        for point in self.points:
            p = Point(x=int(point[0] * context.container_size.width),
                      y=int(context.container_size.height - point[1] * context.container_size.height))
            line_sequence.append(p.xy)

        context.draw.line(
            xy=line_sequence,
            fill=Color.black().rgba,
        )

