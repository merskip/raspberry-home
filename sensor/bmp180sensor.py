from typing import List

from platform.characteristic import Characteristic, Characteristics
from platform.sensor import Sensor
from sensor.impl.bmp180 import bmp180


class BMP180Sensor(Sensor):

    def __init__(self, id: int, name: str, address: int):
        super().__init__(id, name)
        self._sensor = bmp180(address)

    def get_characteristics(self) -> List[Characteristic]:
        return [
            Characteristics.pressure,
            Characteristics.temperature
        ]

    def get_value(self, characteristic: Characteristic) -> object:
        if characteristic == Characteristics.pressure:
            return self._sensor.get_pressure() / 100.0
        elif characteristic == Characteristics.temperature:
            return self._sensor.get_temp()
        else:
            raise ValueError("Unknown characteristic")
