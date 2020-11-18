from enum import Enum
from typing import List

from raspberry_home.view.color import Color
from raspberry_home.view.render import RenderContext
from raspberry_home.view.view import *


class StackDistribution(Enum):
    Start = 'START'
    End = 'END'
    EqualSpacing = 'EQUAL_SPACING'


class StackAlignment(Enum):
    Start = 'START'
    End = 'END'
    Center = 'CENTER'


class _AbsStack(View):

    def __init__(
            self,
            children: List[View],
            spacing: float = 0,
            distribution: StackDistribution = StackDistribution.Start,
            alignment: StackAlignment = StackAlignment.Start
    ):
        self.children = children
        self.spacing = spacing
        self.spacing_count = max(len(children) - 1, 1)
        self.distribution = distribution
        self.alignment = alignment

    def content_size(self, container_size: Size) -> Size:
        main_axis, cross_axis = self.get_axes_content_size(container_size)
        container_main_axis, container_cross_axis = self.size_to_axes(container_size)
        if self.distribution != StackDistribution.Start:
            main_axis = max(main_axis, container_main_axis)

        return self.axes_to_size((main_axis, cross_axis))

    def render(self, context: RenderContext):
        main_axis, cross_axis = self.point_to_axes(context.origin)
        container_main_size, container_cross_size = self.size_to_axes(context.container_size)
        content_main_size, content_cross_size = self.get_axes_content_size(context.container_size)
        spacing_list = [self.spacing] * self.spacing_count

        if self.distribution == StackDistribution.End:
            main_axis += container_main_size - content_main_size
        elif self.distribution == StackDistribution.EqualSpacing:
            content_main_axis, _ = self.get_axes_children_size(context.container_size)
            spacing = (container_main_size - content_main_axis) // self.spacing_count
            spacing_list = [spacing] * self.spacing_count
            if content_main_axis + spacing * self.spacing_count != container_main_size:
                spacing_list[-1] += container_main_size - (content_main_axis + spacing * self.spacing_count)

        if self.distribution != StackDistribution.Start:
            content_main_size, content_cross_size = container_main_size, container_cross_size

        start_main_axis = main_axis
        start_cross_axis = cross_axis
        for index, child in enumerate(self.children):
            content_size = child.content_size(self.axes_to_size((0, container_cross_size)))
            content_main_axis, content_cross_axis = self.size_to_axes(content_size)

            cross_axis = start_cross_axis
            if self.alignment == StackAlignment.End:
                cross_axis += container_cross_size - content_cross_axis
            elif self.alignment == StackAlignment.Center:
                cross_axis += (container_cross_size - content_cross_axis) // 2

            child.render(context.copy(
                origin=self.axes_to_point((main_axis, cross_axis)),
                container_size=content_size
            ))

            if index < len(spacing_list):
                main_axis += content_main_axis + spacing_list[index]
                self.render_view_filled_bounds(
                    context,
                    frame=Rect(
                        origin=self.axes_to_point((main_axis - spacing_list[index], start_cross_axis + 1)),
                        size=self.axes_to_size((spacing_list[index], container_cross_size - 2))
                    ),
                    color=Color(127, 0, 255, 16/255),
                )

        self.render_view_bounds(
            context,
            frame=Rect(
                origin=self.axes_to_point((start_main_axis, start_cross_axis)),
                size=self.axes_to_size((content_main_size, content_cross_size))
            ),
            color=Color(127, 0, 255, 64/255)
        )

    def get_axes_content_size(self, container_size: Size) -> (int, int):
        main_axis, cross_axis = self.get_axes_children_size(container_size)
        main_axis += self.spacing * self.spacing_count
        return main_axis, cross_axis

    def get_axes_children_size(self, container_size: Size) -> (int, int):
        main_axis, cross_axis = 0, 0
        for child in self.children:
            child_main_axis, child_cross_axis = self.size_to_axes(child.content_size(container_size))
            main_axis += child_main_axis
            cross_axis = max(cross_axis, child_cross_axis)
        return main_axis, cross_axis

    def point_to_axes(self, point: Point) -> (int, int):
        return self.size_to_axes(Size(point.x, point.y))

    def axes_to_point(self, axes: (int, int)) -> Point:
        size = self.axes_to_size(axes)
        return Point(x=size.width, y=size.height)

    @abstractmethod
    def size_to_axes(self, size: Size) -> (int, int):
        pass

    @abstractmethod
    def axes_to_size(self, axes: (int, int)) -> Size:
        pass


class VerticalStack(_AbsStack):

    def __init__(
            self,
            children: List[View],
            spacing: float = 0,
            distribution: StackDistribution = StackDistribution.Start,
            alignment: StackAlignment = StackAlignment.Start
    ): super().__init__(children, spacing, distribution, alignment)

    def size_to_axes(self, size: Size) -> (int, int):
        return size.height, size.width

    def axes_to_size(self, axes: (int, int)) -> Size:
        main_axis, cross_axis = axes
        return Size(width=cross_axis, height=main_axis)


class HorizontalStack(_AbsStack):

    def __init__(
            self,
            children: List[View],
            spacing: float = 0,
            distribution: StackDistribution = StackDistribution.Start,
            alignment: StackAlignment = StackAlignment.Start
    ): super().__init__(children, spacing, distribution, alignment)

    def size_to_axes(self, size: Size) -> (int, int):
        return size.width, size.height

    def axes_to_size(self, axes: (int, int)) -> Size:
        main_axis, cross_axis = axes
        return Size(width=main_axis, height=cross_axis)
