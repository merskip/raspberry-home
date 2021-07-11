from functools import partial

from raspberry_home.controller.input_controls import InputControls
from raspberry_home.simulator.simulator_window import SimulatorWindow


class SimulatorInputControls(InputControls):

    def __init__(self, simulator_window: SimulatorWindow):
        super().__init__()
        for index, button in enumerate(simulator_window.buttons):
            button.clicked.connect(partial(self._button_clicked, index))

    def _button_clicked(self, index):
        self._notify_listener_clicked_button(index)
