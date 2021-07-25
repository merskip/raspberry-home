from typing import List, Tuple

from raspberry_home.view.color import Color
from raspberry_home.view.geometry import Size, Point
from raspberry_home.view.render import RenderContext
from raspberry_home.view.view import View


class LineChartSeries:
    def __init__(self,
                 points: List[Tuple[float, float]],
                 color: Color = Color.black(),
                 min_x=None,
                 max_x=None,
                 min_y=None,
                 max_y=None
                 ):
        self.points = points
        self.color = color
        self.min_x = min_x if min_x is not None else min(points, key=lambda p: p[0])[0]
        self.max_x = max_x if max_x is not None else max(points, key=lambda p: p[0])[0]
        self.min_y = min_y if min_y is not None else min(points, key=lambda p: p[1])[1]
        self.max_y = max_y if max_y is not None else max(points, key=lambda p: p[1])[1]

    def to_normalized_points(self) -> List[Tuple[float, float]]:
        return list(map(self._normalize_point, self.points))

    def _normalize_point(self, point: Tuple[float, float]) -> Tuple[float, float]:
        normalized_x = (point[0] - self.min_x) / (self.max_x - self.min_x) if self.max_x != self.min_x else 1
        normalized_y = (point[1] - self.min_y) / (self.max_y - self.min_y) if self.max_y != self.min_y else 1
        return normalized_x, normalized_y


class LineChart(View):

    def __init__(self, series: List[LineChartSeries]):
        self.series = series

    def content_size(self, container_size: Size) -> Size:
        return container_size

    def render(self, context: RenderContext):
        for series in self.series:
            raw_line_view = _RawLineView(
                points=series.to_normalized_points()
            )
            raw_line_view.render(context.copy())


class _RawLineView(View):

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
