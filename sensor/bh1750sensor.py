from typing import List

from platform.sensor import Sensor, Characteristic, Characteristics
from sensor.impl import bh1750


class BH1750Sensor(Sensor):

    def __init__(self, name: str, address: int):
        super().__init__(name)
        self._address = address

    def get_characteristics(self) -> List[Characteristic]:
        return [Characteristics.light]

    def get_value(self, characteristic: Characteristic) -> object:
        return bh1750.readLight(self._address)
