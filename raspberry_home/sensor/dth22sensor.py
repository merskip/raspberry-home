from typing import List

import adafruit_dht

from raspberry_home.platform.characteristic import Characteristic, Characteristics
from raspberry_home.platform.sensor import Sensor


class DTH22Sensor(Sensor):

    def __init__(self, id: int, name: str, pin):
        super().__init__(id, name)
        self._dht22 = adafruit_dht.DHT22(pin)

    def get_characteristics(self) -> List[Characteristic]:
        return [
            Characteristics.humidity.set(min_value=0, max_value=95, accuracy=2)
        ]

    def get_value(self, characteristic: Characteristic) -> object:
        if characteristic == Characteristics.humidity:
            return self._dht22.humidity
        else:
            return self._dht22.temperature
