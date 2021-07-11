
from raspberry_home.controller.home_controller import Fonts
from raspberry_home.controller.input_controller import NavigationItem
from raspberry_home.display.display import Display
from raspberry_home.view.center import Center
from raspberry_home.view.text import Text


class ChartController(NavigationItem):

    def __init__(self, display: Display):
        self.display = display

    def selected_show(self):
        self.display.set_view(
            root_view=Center(
                child=Text("Chart controller")
            )
        )
