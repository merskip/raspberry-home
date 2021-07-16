import sys

from PyQt5.QtWidgets import QApplication

from raspberry_home.components_provider import ComponentsProvider
from raspberry_home.controller.input_controls import InputControls
from raspberry_home.database.DatabaseWriter import DatabaseWriter
from raspberry_home.database.sqllite_repository import SqliteRepository
from raspberry_home.display.display import Display
from raspberry_home.platform.characteristic import Characteristics
from raspberry_home.platform.measurements_scheduler import MeasurementsListener
from raspberry_home.platform.sensor import Sensor
from raspberry_home.simulator.simulator_display import SimulatorDisplay
from raspberry_home.simulator.simulator_input_controls import SimulatorInputControls
from raspberry_home.simulator.simulator_window import SimulatorWindow
from raspberry_home.stub.stub_platform import StubPlatform
from raspberry_home.view.renderable import Renderable


class SimulatorComponentsProvider(ComponentsProvider):

    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.simulator_window = SimulatorWindow()
        self.display = SimulatorDisplay((264, 176), self.simulator_window)
        self.input_controls = SimulatorInputControls(self.simulator_window)

        self.simulator_window.frames_check_box.stateChanged.connect(self.handle_toggles_frames)
        self.simulator_window.rgb_check_box.stateChanged.connect(self.handle_toggles_rgb)

        self.repository = SqliteRepository(filename="database.sqlite")

    def on_measurement_begin(self):
        self.repository.update(sensors=self.get_sensors())
        self.simulator_window.show()
        self.app.exec()

    def get_display(self) -> Display:
        return self.display

    def get_sensors(self) -> [Sensor]:
        return StubPlatform().get_sensors()  # TODO: Remove Platform class

    def get_measurements_listeners(self) -> [MeasurementsListener]:
        return [self.repository]

    def get_scheduler_time_intervals(self) -> int:
        return 10  # 10 seconds

    def handle_toggles_frames(self, check_state):
        is_checked = check_state == 2
        Renderable.set_show_frames(is_checked)
        self.display.refresh()

    def handle_toggles_rgb(self, _):
        self.display.refresh()

    def get_input_controls(self) -> InputControls:
        return self.input_controls
