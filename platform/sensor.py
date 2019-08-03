import copy
from abc import ABC, abstractmethod
from typing import List


class Characteristic:

    def __init__(self, name: str, unit: str = None, scale: float = 1.0):
        self.name = name
        self.unit = unit
        self.scale = scale
        self.specific_type = None

    def toggle(self, specific_type: str, enabled: bool = True):
        if enabled and specific_type is not None:
            new_characteristic = copy.copy(self)
            new_characteristic.specific_type = specific_type
            return new_characteristic
        else:
            return self

    def __eq__(self, other):
        return self.name == other.name


class Characteristics(object):
    temperature = Characteristic("temperature", "°C")
    humidity = Characteristic("humidity", "%", scale=100.0)
    light = Characteristic("light", "lx")
    pressure = Characteristic("pressure", "hPa", scale=0.01)
    boolean = Characteristic("boolean")


class SpecificType(object):
    temperature_outside = "outside"
    boolean_door = "door"


class Sensor(ABC):

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def get_characteristics(self) -> List[Characteristic]:
        pass

    def get_value_with_unit(self, characteristic: Characteristic) -> str:
        value = self.get_value(characteristic)
        return self.format_value_with_unit(characteristic, value)

    @abstractmethod
    def get_value(self, characteristic: Characteristic) -> object:
        pass

    @staticmethod
    def format_value_with_unit(characteristic: Characteristic, value):
        if isinstance(value, float):
            value = "%.2f" % (value * characteristic.scale)
        if isinstance(value, bool):
            value = value if "True" else "False"
        if characteristic.unit is not None:
            return "%s %s" % (value, characteristic.unit)
        else:
            return str(value)
