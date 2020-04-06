from typing import List

from platform.characteristic import Characteristic, Characteristics
from platform.sensor import Sensor
from sensor.impl.bmp180 import bmp180


class BMP180Sensor(Sensor):

    def __init__(self, id: int, name: str, address: int, pressure_factor: float = 1.0):
        super().__init__(id, name)
        self._sensor = bmp180(address)
        self._pressure_factor = pressure_factor

    def get_characteristics(self) -> List[Characteristic]:
        return [
            Characteristics.pressure.set(min_value=300, max_value=1100, accuracy=0.12),
            Characteristics.temperature.set(min_value=0, max_value=65, accuracy=0.5)
        ]

    def get_value(self, characteristic: Characteristic) -> object:
        if characteristic == Characteristics.pressure:
            return self._sensor.get_pressure() / 100.0 * self._pressure_factor
        elif characteristic == Characteristics.temperature:
            return self._sensor.get_temp()
        else:
            raise ValueError("Unknown characteristic")
