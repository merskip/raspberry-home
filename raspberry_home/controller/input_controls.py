from abc import ABC, abstractmethod


class InputControls(ABC):

    class Listener(ABC):

        @abstractmethod
        def on_clicked_button(self, index: int):
            pass

    def __init__(self):
        self.listeners = []

    def add_listener(self, listener: Listener):
        self.listeners.append(listener)

    def _notify_listener_clicked_button(self, index: int):
        for listener in self.listeners:
            listener.on_clicked_button(index=index)