from typing import List

from platform.sensor import Sensor, Characteristic, Characteristics
import Adafruit_DHT


class DTH11Sensor(Sensor):

    def __init__(self, name: str, pin: int):
        super().__init__(name)
        self._pin = pin

    def get_characteristics(self) -> List[Characteristic]:
        return [Characteristics.humidity]

    def get_value(self, characteristic: Characteristic) -> object:
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, self._pin)
        return humidity / 100.0
