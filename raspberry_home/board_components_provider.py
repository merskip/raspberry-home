from raspberry_home.display.display import Display
from raspberry_home.components_provider import ComponentsProvider
from raspberry_home.platform.measurements_scheduler import MeasurementsListener
from raspberry_home.platform.sensor import Sensor


class BoardComponentsProvider(ComponentsProvider):

    def get_display(self) -> Display:
        pass

    def get_sensors(self) -> [Sensor]:
        pass

    def get_measurements_listeners(self) -> [MeasurementsListener]:
        pass

