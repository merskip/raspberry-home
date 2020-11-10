from typing import List

from raspberry_home.view.view import *


class ZStack(View):

    def __init__(self, children: List[View]):
        self.children = children

    def content_size(self, container_size: Size) -> Size:
        width, height = 0, 0
        for child in self.children:
            content_size = child.content_size(container_size)
            width = max(width, content_size.width)
            height = max(height, content_size.height)
        return Size(width, height)

    def render(self, context: RenderContext):
        for child in self.children:
            child.render(context)
