from abc import ABC, abstractmethod
from configparser import ConfigParser

from raspberry_home.display.display import Display
from raspberry_home.platform.measurements_scheduler import MeasurementsListener
from raspberry_home.platform.sensor import Sensor


class ComponentsProvider(ABC):

    def __init__(self):
        self.config = ConfigParser()
        if not self.config.read("config.ini"):
            raise RuntimeError("Failed read config file: config.ini")

    @abstractmethod
    def get_display(self) -> Display:
        pass

    @abstractmethod
    def get_sensors(self) -> [Sensor]:
        pass

    @abstractmethod
    def get_measurements_listeners(self) -> [MeasurementsListener]:
        pass

    @abstractmethod
    def get_scheduler_time_intervals(self) -> int:
        pass
