from abc import ABC, abstractmethod
from typing import List


class InputControls(ABC):

    class Listener(ABC):

        @abstractmethod
        def on_clicked_button(self, index: int):
            pass

    listeners: List[Listener] = []

    def add_listener(self, listener: Listener):
        self.listeners.append(listener)
