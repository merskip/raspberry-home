from enum import Enum
from typing import List

from raspberry_home.view.color import Color
from raspberry_home.view.render import RenderContext
from raspberry_home.view.view import *


class StackDistribution(Enum):
    Start = 'START'
    End = 'END'
    Equal = 'EQUAL'


class StackAlignment(Enum):
    Start = 'START'
    End = 'END'
    Center = 'CENTER'


class AxisSize:

    def __init__(self, main_size: int, cross_size: int):
        self.main_size = main_size
        self.cross_size = cross_size


class AxisPoint:

    def __init__(self, main_axis: int, cross_axis: int):
        self.main_axis = main_axis
        self.cross_axis = cross_axis


class _StackItem:
    is_view = property(lambda self: self.view is not None)
    is_spacing = property(lambda self: self.spacing is not None)

    def __init__(self, main_axis: int, main_size: int):
        self.main_axis = main_axis
        self.main_size = main_size
        self.view = None
        self.spacing = None
        self.content_size = None
        self.container_size = None

    @staticmethod
    def view(view: View, main_axis: int, content_size: AxisSize, container_size: Size):
        item = _StackItem(main_axis, content_size.main_size)
        item.view = view
        item.content_size = content_size
        item.container_size = container_size
        return item

    @staticmethod
    def spacing(spacing: int, main_axis: int):
        item = _StackItem(main_axis, spacing)
        item.spacing = spacing
        return item


class _StackLayout:

    def __init__(self, items: [_StackItem], container_size: AxisSize, max_main_size: bool):
        self.items = items
        self.container_size = container_size
        main_size, cross_size = 0, 0
        for item in items:
            main_size += item.main_size
            if item.is_view:
                cross_size = max(cross_size, item.content_size.cross_size)
        self.content_size = AxisSize(container_size.main_size if max_main_size else main_size, cross_size)


class _Stack(View, ABC):

    def __init__(
            self,
            children: List[View],
            spacing: int = 0,
            distribution: StackDistribution = StackDistribution.Start,
            alignment: StackAlignment = StackAlignment.Start
    ):
        self.children = children
        self.spacing = spacing
        self.distribution = distribution
        self.alignment = alignment

    def _calculate_layout(self, container_size: Size) -> _StackLayout:
        if self.distribution == StackDistribution.Start:
            return self._calculate_layout_start_distribution(self.size_to_axes(container_size))
        elif self.distribution == StackDistribution.End:
            return self._calculate_layout_end_distribution(self.size_to_axes(container_size))
        elif self.distribution == StackDistribution.Equal:
            return self._calculate_layout_equal_distribution(self.size_to_axes(container_size))
        else:
            raise ValueError("distribution has illegal value: %s" % self.distribution)

    def _calculate_layout_start_distribution(self, container_size: AxisSize) -> _StackLayout:
        items = []
        next_item_main_axis = 0
        for child in self.children:
            remaining_main_size = container_size.main_size - next_item_main_axis
            child_container_size = self.axes_to_size(AxisSize(remaining_main_size, container_size.cross_size))
            child_content_size = self.size_to_axes(child.content_size(child_container_size))
            items.append(_StackItem.view(child, next_item_main_axis, child_content_size, child_container_size))

            items.append(_StackItem.spacing(self.spacing, next_item_main_axis + child_content_size.main_size))
            next_item_main_axis += child_content_size.main_size + self.spacing
        items.pop()

        return _StackLayout(items, container_size, max_main_size=False)

    def _calculate_layout_end_distribution(self, container_size: AxisSize) -> _StackLayout:
        items = []
        next_item_end_main_axis = container_size.main_size
        for child in list(reversed(self.children)):
            child_container_size = self.axes_to_size(AxisSize(next_item_end_main_axis, container_size.cross_size))
            child_content_size = self.size_to_axes(child.content_size(child_container_size))
            item_main_axis = next_item_end_main_axis - child_content_size.main_size
            items.append(_StackItem.view(child, item_main_axis,
                                         child_content_size, child_container_size))

            items.append(_StackItem.spacing(self.spacing, item_main_axis - self.spacing))
            next_item_end_main_axis -= child_content_size.main_size + self.spacing
        items.pop()

        return _StackLayout(items, container_size, max_main_size=True)

    def _calculate_layout_equal_distribution(self, container_size: AxisSize) -> _StackLayout:
        items = []
        available_container_main_size = container_size.main_size - self.spacing * (len(self.children) - 1)
        child_content_main_size = available_container_main_size // len(self.children)
        next_item_main_axis = 0
        child_container_size = self.axes_to_size(AxisSize(child_content_main_size, container_size.cross_size))
        for child in self.children:
            child_content_size = self.size_to_axes(child.content_size(child_container_size))
            items.append(_StackItem.view(child, next_item_main_axis,
                                         child_content_size, child_container_size))

            items.append(_StackItem.spacing(self.spacing, next_item_main_axis + child_content_main_size))
            next_item_main_axis += child_content_main_size + self.spacing
        items.pop()

        return _StackLayout(items, container_size, max_main_size=True)

    def content_size(self, container_size: Size) -> Size:
        layout = self._calculate_layout(container_size)
        return self.axes_to_size(layout.content_size)

    def render(self, context: RenderContext):
        layout = self._calculate_layout(context.container_size)
        for item in layout.items:
            if item.is_view:
                item.view.render(context.copy(
                    origin=context.origin + self._get_item_origin(layout, item),
                    container_size=item.container_size
                ))
            else:
                if item.spacing > 0:
                    self.render_view_filled_bounds(
                        context,
                        frame=Rect(context.origin + self.axes_to_point(AxisPoint(item.main_axis, 0)),
                                   self.axes_to_size(AxisSize(item.main_size, layout.content_size.cross_size))),
                        color=Color.red().copy(alpha=0.05),
                    )
        self.render_view_bounds(
            context,
            frame=Rect(context.origin, self.axes_to_size(layout.content_size)),
            color=Color.red().copy(alpha=0.4),
        )

    def _get_item_origin(self, layout: _StackLayout, item: _StackItem) -> Point:
        if self.alignment == StackAlignment.Start:
            return self.axes_to_point(AxisPoint(item.main_axis, 0))
        elif self.alignment == StackAlignment.Center:
            cross_axis = (layout.content_size.cross_size - item.content_size.cross_size) // 2
            return self.axes_to_point(AxisPoint(item.main_axis, cross_axis))
        elif self.alignment == StackAlignment.End:
            cross_axis = layout.container_size.cross_size - item.content_size.cross_size
            return self.axes_to_point(AxisPoint(item.main_axis, cross_axis))
        else:
            raise ValueError("alignment has illegal value: %s" % self.alignment)

    def point_to_axes(self, point: Point) -> AxisPoint:
        axes = self.size_to_axes(Size(point.x, point.y))
        return AxisPoint(axes.main_size, axes.cross_size)

    def axes_to_point(self, point: AxisPoint) -> Point:
        axes = self.axes_to_size(AxisSize(point.main_axis, point.cross_axis))
        return Point(axes.width, axes.height)

    @abstractmethod
    def size_to_axes(self, size: Size) -> AxisSize:
        pass

    @abstractmethod
    def axes_to_size(self, size: AxisSize) -> Size:
        pass


class VerticalStack(_Stack):

    def __init__(
            self,
            children: List[View],
            spacing: int = 0,
            distribution: StackDistribution = StackDistribution.Start,
            alignment: StackAlignment = StackAlignment.Start
    ): super().__init__(children, spacing, distribution, alignment)

    def size_to_axes(self, size: Size) -> AxisSize:
        return AxisSize(size.height, size.width)

    def axes_to_size(self, size: AxisSize) -> Size:
        return Size(size.cross_size, size.main_size)


class HorizontalStack(_Stack):

    def __init__(
            self,
            children: List[View],
            spacing: int = 0,
            distribution: StackDistribution = StackDistribution.Start,
            alignment: StackAlignment = StackAlignment.Start
    ): super().__init__(children, spacing, distribution, alignment)

    def size_to_axes(self, size: Size) -> AxisSize:
        return AxisSize(size.width, size.height)

    def axes_to_size(self, size: AxisSize) -> Size:
        return Size(size.main_size, size.cross_size)
