from typing import List

from w1thermsensor import W1ThermSensor

from raspberry_home.platform.characteristic import Characteristic, Characteristics
from raspberry_home.platform.sensor import Sensor


class DS18B20Sensor(Sensor):

    def __init__(self, id: int, name: str, device_id: str):
        """
        :type device_id: Device identifier for wire-1, eg. 01186e6706ff
        """
        super().__init__(id, name)
        self._sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, device_id)

    def get_characteristics(self) -> List[Characteristic]:
        return [
            Characteristics.temperature.set(min_value=-55.0, max_value=125, accuracy=0.5)
        ]

    def get_value(self, characteristic: Characteristic) -> object:
        return self._sensor.get_temperature()
