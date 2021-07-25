from raspberry_home.board.gpio_input_controls import GPIOInputControls
from raspberry_home.components_provider import ComponentsProvider
from raspberry_home.controller.input_controls import InputControls
from raspberry_home.database.sqllite_repository import SqliteRepository
from raspberry_home.display.display import Display
from raspberry_home.display.epd.epd2in7_display import EPD2in7Display
from raspberry_home.platform.measurements_scheduler import MeasurementsListener
from raspberry_home.platform.sensor import Sensor
from raspberry_home.platform_impl import PlatformImpl


class BoardComponentsProvider(ComponentsProvider):

    def __init__(self):
        super().__init__()
        self.repository = SqliteRepository(filename="database.sqlite")

    def get_input_controls(self) -> InputControls:
        return GPIOInputControls()

    def on_measurement_begin(self):
        pass

    def get_display(self) -> Display:
        return EPD2in7Display()

    def get_sensors(self) -> [Sensor]:
        return PlatformImpl().get_sensors()

    def get_measurements_listeners(self) -> [MeasurementsListener]:
        return [self.repository]

    def get_scheduler_time_intervals(self) -> int:
        return 10 * 60  # 10 minutes
