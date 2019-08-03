from abc import ABC, abstractmethod
from typing import List

from platform.characteristic import Characteristic


class Sensor(ABC):

    def __init__(self, id: int, name: str):
        self._id = id
        self.name = name
        self.flags = []

    def with_flag(self, flag: str):
        self.flags.append(flag)
        return self

    def has_flag(self, flag: str):
        return flag in self.flags

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
            value = "%.2f" % value
        if isinstance(value, bool):
            value = value if "True" else "False"
        if characteristic.unit is not None:
            return "%s %s" % (value, characteristic.unit)
        else:
            return str(value)

    @property
    def id(self):
        return self._id
