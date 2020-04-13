from typing import List

import Adafruit_DHT

from platform.characteristic import Characteristic, Characteristics
from platform.sensor import Sensor


class DTH11Sensor(Sensor):

    def __init__(self, id: int, name: str, pin: int):
        super().__init__(id, name)
        self._pin = pin

    def get_characteristics(self) -> List[Characteristic]:
        return [
            Characteristics.humidity.set(min_value=5, max_value=95, accuracy=4),
            Characteristics.temperature.set(min_value=-20, max_value=50, accuracy=1)
        ]

    def get_value(self, characteristic: Characteristic) -> object:
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, self._pin)
        if characteristic == Characteristics.humidity:
            return humidity
        else:
            return temperature
