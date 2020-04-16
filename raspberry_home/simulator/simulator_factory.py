from raspberry_home.controller.home_controller import HomeController
from raspberry_home.display.display import Display
from raspberry_home.factory import Factory
from raspberry_home.platform.measurements_scheduler import MeasurementsListener
from raspberry_home.platform.sensor import Sensor
from raspberry_home.simulator.simulator_display import SimulatorDisplay
from raspberry_home.simulator.simulator_window import SimulatorWindow
from raspberry_home.stub.stub_platform import StubPlatform


class SimulatorFactory(Factory):

    def __init__(self):
        super().__init__()
        self.simulator_window = SimulatorWindow()
        self.home_controller = HomeController()

    def get_display(self) -> Display:
        return SimulatorDisplay((264, 176), self.simulator_window)

    def get_sensors(self) -> [Sensor]:
        return StubPlatform().get_sensors()  # TODO: Remove Platform class

    def get_measurements_listeners(self) -> [MeasurementsListener]:
        pass
