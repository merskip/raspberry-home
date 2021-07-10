from typing import List

import adafruit_dht

from raspberry_home.platform.characteristic import Characteristic, Characteristics
from raspberry_home.platform.sensor import Sensor


class DTH22Sensor(Sensor):

    def __init__(self, id: int, name: str, pin):
        super().__init__(id, name)
        self._pin = pin

    def get_characteristics(self) -> List[Characteristic]:
        return [
            Characteristics.humidity.set(min_value=0, max_value=95, accuracy=2)
        ]

    def get_value(self, characteristic: Characteristic) -> object:
        result = adafruit_dht.DHT22(self._pin, use_pulseio=False)
        if characteristic == Characteristics.humidity:
            return result.humidity
        else:
            return result.temperature
