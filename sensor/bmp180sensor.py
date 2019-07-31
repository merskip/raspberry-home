from typing import List

from platform.sensor import Sensor, Characteristic, Characteristics
from sensor.impl.bmp180 import bmp180


class BMP180Sensor(Sensor):

    def __init__(self, name: str, address: int):
        super().__init__(name)
        self._sensor = bmp180(address)

    def get_characteristics(self) -> List[Characteristic]:
        return [
            Characteristics.pressure,
            Characteristics.temperature
        ]

    def get_value(self, characteristic: Characteristic) -> object:
        if characteristic == Characteristics.pressure:
            return self._sensor.get_pressure()
        elif characteristic == Characteristics.temperature:
            return self._sensor.get_temp()
        else:
            raise ValueError("Unknown characteristic")
