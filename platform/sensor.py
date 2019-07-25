from abc import ABC, abstractmethod
from typing import List


class Characteristic:

    def __init__(self, name: str, unit: str = None):
        self.name = name
        self.unit = unit


class Characteristics(object):
    temperature = Characteristic("temperature", "°C")
    light = Characteristic("light", "lx")
    pressure = Characteristic("pressure", "Pa")
    door = Characteristic("door")


class Sensor(ABC):

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def get_characteristics(self) -> List[Characteristic]:
        pass

    @abstractmethod
    def get_value(self, characteristic: Characteristic) -> object:
        pass


