from abc import ABC, abstractmethod

from raspberry_home.view.view import View


class Widget(ABC, View):

    @abstractmethod
    def build(self) -> View:
        pass
