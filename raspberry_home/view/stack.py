from enum import Enum
from typing import List

from raspberry_home.view.view import *


class StackDistribution(Enum):
    Start = 'START'
    End = 'END'
    EqualSpacing = 'EQUAL_SPACING'


class HorizontalStack(View):

    def __init__(
            self,
            children: List[View],
            spacing: float = 0,
            distribution: StackDistribution = StackDistribution.Start
    ):
        self.children = children
        self.spacing = spacing
        self.distribution = distribution

    def content_size(self, container_size: Size) -> Size:
        width, height = 0, 0
        for child in self.children:
            content_size = child.content_size(container_size)
            width += content_size.width
            height = max(height, content_size.height)
        width += (len(self.children) - 1) * self.spacing
        return Size(width, height)

    def render(self, context: RenderContext):
        x, y = context.origin.xy
        if self.distribution == StackDistribution.End:
            content_size = self.content_size(context.container_size)
            x = context.container_size.width - content_size.width
            spacing = self.spacing
        elif self.distribution == StackDistribution.EqualSpacing:
            width = 0
            for child in self.children:
                width += child.content_size(context.container_size).width
            spacing = (context.container_size.width - width) // (len(self.children) - 1)
        else:
            spacing = self.spacing

        for child in self.children:
            content_size = child.content_size(context.container_size)
            if self.distribution == StackDistribution.EqualSpacing and child == self.children[-1]:
                x = context.container_size.width - content_size.width

            child.render(context.copy(
                origin=Point(x=x, y=y)
            ))
            x += content_size.width + spacing


class VerticalStack(View):

    def __init__(self, children: List[View], spacing: float = 0):
        self.children = children
        self.spacing = spacing

    def content_size(self, container_size: Size) -> Size:
        width, height = 0, 0
        for child in self.children:
            content_size = child.content_size(container_size)
            width = max(width, content_size.width)
            height += content_size.height
        height += (len(self.children) - 1) * self.spacing
        return Size(width, height)

    def render(self, context: RenderContext):
        x, y = context.origin.xy
        for child in self.children:
            content_size = child.content_size(context.container_size)
            child.render(context.copy(
                origin=Point(x=x, y=y)
            ))
            y += content_size.height + self.spacing
