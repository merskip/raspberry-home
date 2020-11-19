from __future__ import annotations

from abc import ABC, abstractmethod

from raspberry_home.view.geometry import *
from raspberry_home.view.renderable import Renderable


class View(Renderable, ABC):

    @abstractmethod
    def content_size(self, container_size: Size) -> Size:
        pass
