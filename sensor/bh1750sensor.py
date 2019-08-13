from typing import List

from platform.characteristic import Characteristic, Characteristics
from platform.sensor import Sensor
from sensor.impl import bh1750


class BH1750Sensor(Sensor):

    def __init__(self, id: int, name: str, address: int):
        super().__init__(id, name)
        self._address = address

    def get_characteristics(self) -> List[Characteristic]:
        return [
            Characteristics.light.set(min_value=1, max_value=65535, accuracy=1)
        ]

    def get_value(self, characteristic: Characteristic) -> object:
        return bh1750.readLight(self._address)
