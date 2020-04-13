import math
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
        return self.formatted_value_with_unit(characteristic, value)

    @abstractmethod
    def get_value(self, characteristic: Characteristic) -> object:
        pass

    def is_storable(self):
        return True

    # TODO: Move to new class - ValueFormatter
    @staticmethod
    def formatted_value_with_unit(characteristic: Characteristic, value):
        formatted_value = Sensor.formatted_value(characteristic, value)
        if characteristic.unit is not None:
            return "{} {}".format(formatted_value, characteristic.unit)
        else:
            return formatted_value

    @staticmethod
    def formatted_value(characteristic: Characteristic, value):
        if isinstance(value, bool):
            return value if "True" else "False"
        elif isinstance(value, float):
            if isinstance(characteristic.accuracy, float):
                value = Sensor.round_value(value, characteristic.min_value, characteristic.accuracy)
                return Sensor.format_value_to_string(value, characteristic.accuracy)
            else:
                return "{:.2f}".format(value)
        elif isinstance(value, list):
            return "/".join(map(str, value))
        else:
            return str(value)

    @staticmethod
    def round_value(value, min_value: float, accuracy: float):
        if not isinstance(value, float) or min_value is None or accuracy is None:
            return value

        rounded_value = math.floor((value - min_value) / accuracy) * accuracy + min_value
        if value - rounded_value >= accuracy / 2.0:
            rounded_value += accuracy
        return rounded_value

    @staticmethod
    def format_value_to_string(value, accuracy: float):
        if not isinstance(value, float):
            return value
        if accuracy % 1 == 0:  # Accuracy is integer
            return "{:.0f}".format(value)

        decimal_part = "{}".format(accuracy).split('.')[1]
        decimal_places = len(decimal_part)
        return ("{:.%df}" % decimal_places).format(value)

    @property
    def id(self):
        return self._id
