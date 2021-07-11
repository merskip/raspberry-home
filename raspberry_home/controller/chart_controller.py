
from raspberry_home.view.center import Center
from raspberry_home.view.text import Text
from raspberry_home.view.view import View
from raspberry_home.view.widget import Widget


class ChartController(Widget):

    def build(self) -> View:
        return Center(
            child=Text("Chart controller")
        )
