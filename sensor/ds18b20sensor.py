from typing import List

from w1thermsensor import W1ThermSensor

from platform.sensor import Sensor, Characteristic, Characteristics, SpecificType


class DS18B20Sensor(Sensor):

    def __init__(self, name: str, device_id: str, is_outside: bool = False):
        """
        :type device_id: Device identifier for wire-1, eg. 01186e6706ff
        """
        super().__init__(name)
        self._sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, device_id)
        self.is_outside = is_outside

    def get_characteristics(self) -> List[Characteristic]:
        return [Characteristics.temperature.toggle(SpecificType.temperature_outside, self.is_outside)]

    def get_value(self, characteristic: Characteristic) -> object:
        return self._sensor.get_temperature()
