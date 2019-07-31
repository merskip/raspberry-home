from typing import List

import RPi.GPIO as GPIO
from platform.sensor import Sensor, Characteristic, Characteristics


class GPIOSensor(Sensor):

    def __init__(self, name: str, pin: int, specific_type: str = None):
        super().__init__(name)
        self._pin = pin
        self._specific_type = specific_type

        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def __del__(self):
        GPIO.cleanup(self._pin)

    def get_characteristics(self) -> List[Characteristic]:
        return [Characteristics.boolean.toggle(self._specific_type)]

    def get_value(self, characteristic: Characteristic) -> object:
        return GPIO.input(self._pin) == 1
