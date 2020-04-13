from typing import Callable, List

from raspberry_home.platform.characteristic import Characteristic
from raspberry_home.platform.sensor import Sensor


class StubSensor(Sensor):

    def __init__(self, id: int, name: str, characteristics: List[Characteristic],
                 get_value: Callable[[Characteristic], object]):
        super().__init__(id, name)
        self._characteristics = characteristics
        self._get_value = get_value

    def get_characteristics(self) -> List[Characteristic]:
        return self._characteristics

    def get_value(self, characteristic: Characteristic) -> object:
        return self._get_value(characteristic)
