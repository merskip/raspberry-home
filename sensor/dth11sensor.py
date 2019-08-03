from typing import List

import Adafruit_DHT

from platform.characteristic import Characteristic, Characteristics
from platform.sensor import Sensor


class DTH11Sensor(Sensor):

    def __init__(self, id: int, name: str, pin: int):
        super().__init__(id, name)
        self._pin = pin

    def get_characteristics(self) -> List[Characteristic]:
        return [Characteristics.humidity]

    def get_value(self, characteristic: Characteristic) -> object:
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, self._pin)
        return humidity
