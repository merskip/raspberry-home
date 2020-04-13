from typing import List

from raspberry_home.platform.sensor import Sensor


class Platform(object):

    def __init__(self, sensors: List[Sensor]):
        self._sensors = sensors

    def get_sensors(self) -> List[Sensor]:
        return self._sensors
