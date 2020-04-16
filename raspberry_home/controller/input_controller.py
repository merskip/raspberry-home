from abc import ABC, abstractmethod

from raspberry_home.controller.input_controls import InputControls


class NavigationItem(ABC):

    @abstractmethod
    def selected_show(self):
        pass


class InputController(InputControls.Listener):

    def __init__(self, items: [NavigationItem]):
        self.items = items

    def on_clicked_button(self, index: int):
        self.items[index].selected_show()
