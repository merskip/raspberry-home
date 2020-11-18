from raspberry_home.components_provider import ComponentsProvider
from raspberry_home.display.display import Display
from raspberry_home.display.epd.epd2in7_display import EPD2in7Display
from raspberry_home.platform.measurements_scheduler import MeasurementsListener
from raspberry_home.platform.sensor import Sensor
from raspberry_home.platform_impl import PlatformImpl


class BoardComponentsProvider(ComponentsProvider):

    def on_measurement_begin(self):
        pass

    def get_display(self) -> Display:
        return EPD2in7Display()

    def get_sensors(self) -> [Sensor]:
        return PlatformImpl().get_sensors()

    def get_measurements_listeners(self) -> [MeasurementsListener]:
        return []

    def get_scheduler_time_intervals(self) -> int:
        return 10 * 60  # 10 minutes
