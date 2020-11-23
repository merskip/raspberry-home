from datetime import datetime

from raspberry_home.platform.characteristic import Characteristic
from raspberry_home.platform.sensor import Sensor


class Measurement:

    def __init__(self, sensor: Sensor, characteristic: Characteristic, value,
                 time_start: datetime, time_end: datetime):
        self.sensor = sensor
        self.characteristic = characteristic
        self.value = value
        self.time_start = time_start
        self.time_end = time_end

    def is_primary(self):
        return self.sensor.get_characteristics()[0] == self.characteristic
