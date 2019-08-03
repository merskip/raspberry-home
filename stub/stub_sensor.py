from typing import Callable, List

from platform.sensor import Sensor, Characteristic


class StubSensor(Sensor):

    def __init__(self, name: str, characteristics: List[Characteristic],
                 get_value: Callable[[Characteristic], object]):
        super().__init__(name)
        self._characteristics = characteristics
        self._get_value = get_value

    def get_characteristics(self) -> List[Characteristic]:
        return self._characteristics

    def get_value(self, characteristic: Characteristic) -> object:
        return self._get_value(characteristic)
