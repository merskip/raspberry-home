from raspberry_home.controller.home_controller import HomeController
from raspberry_home.display.display import Display
from raspberry_home.components_provider import ComponentsProvider
from raspberry_home.platform.measurements_scheduler import MeasurementsListener
from raspberry_home.platform.sensor import Sensor
from raspberry_home.simulator.simulator_display import SimulatorDisplay
from raspberry_home.simulator.simulator_window import SimulatorWindow
from raspberry_home.stub.stub_platform import StubPlatform


class SimulatorComponentsProvider(ComponentsProvider):

    def __init__(self):
        super().__init__()
        self.simulator_window = SimulatorWindow()
        self.display = SimulatorDisplay((264, 176), self.simulator_window)
        self.home_controller = HomeController(
            display=self.display,
            # TODO: Move to config.ini
            coordinates={'longitude': 22.4937312, 'latitude': 51.2181956},  # Lublin
            timezone_offset=7200 # UTC+2
        )

    def get_display(self) -> Display:
        return self.display

    def get_sensors(self) -> [Sensor]:
        return StubPlatform().get_sensors()  # TODO: Remove Platform class

    def get_measurements_listeners(self) -> [MeasurementsListener]:
        pass

    def get_scheduler_time_intervals(self) -> int:
        return 60  # 1 minute
