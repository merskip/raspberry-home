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

    def get_value_with_unit(self, characteristic: Characteristic) -> str:
        value = self.get_value(characteristic)
        if characteristic.unit is not None:
            return "%s %s" % (value, characteristic.unit)
        else:
            return str(value)

    @abstractmethod
    def get_value(self, characteristic: Characteristic) -> object:
        pass


