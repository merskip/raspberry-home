from typing import List

import RPi.GPIO as GPIO

from raspberry_home.platform.characteristic import Characteristic, Characteristics
from raspberry_home.platform.sensor import Sensor


class GPIOSensor(Sensor):

    def __init__(self, id: int, name: str, pin: int):
        super().__init__(id, name)
        self._pin = pin

        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def __del__(self):
        GPIO.cleanup(self._pin)

    def get_characteristics(self) -> List[Characteristic]:
        return [Characteristics.boolean]

    def get_value(self, characteristic: Characteristic) -> object:
        return GPIO.input(self._pin) == 1
