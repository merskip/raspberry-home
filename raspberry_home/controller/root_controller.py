from typing import List

from raspberry_home.controller.input_controls import InputControls
from raspberry_home.display.display import Display
from raspberry_home.logger import Logger
from raspberry_home.platform.measurement import Measurement
from raspberry_home.platform.measurements_scheduler import MeasurementsListener
from raspberry_home.view.widget import Widget


class RootController(InputControls.Listener, MeasurementsListener):

    logger = Logger("RootController")

    def __init__(self, display: Display, screens: List[Widget]):
        self.display = display
        self.screens = screens
        self._show_screen_at_index(0)

    def on_clicked_button(self, index: int):
        self._show_screen_at_index(index)

    def on_measurements(self, measurements: List[Measurement]):
        self._refresh_current_screen()

    def _refresh_current_screen(self):
        self._show_screen_at_index(self.current_screen_index)

    def _show_screen_at_index(self, index: int):
        if index < len(self.screens):
            self.logger.info("Showing screen at index %d" % index)
            self.display.set_view(
                root_view=self.screens[index]
            )
            self.current_screen_index = index
        else:
            self.logger.warning("No screen at index %d" % index)
