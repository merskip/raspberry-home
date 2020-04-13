import time
from typing import List

from platform.characteristic import Characteristic, Characteristics
from platform.sensor import Sensor

import serial


class SoilMoistureSensor(Sensor):

    def __init__(self, id: int, name: str, port: str, baudrate: int, pin: int):
        super().__init__(id, name)
        self._port = port
        self._baudrate = baudrate
        self._pin = pin
        self._minValue = 0.3
        self._maxValue = 0.9

    def get_characteristics(self) -> List[Characteristic]:
        return [Characteristics.soilMoisture.set(min_value=0, max_value=100, accuracy=1)]

    def get_value(self, characteristic: Characteristic):
        value = self._request_pin_value(self._pin)
        normalized_value = 1 - (value - self._minValue) / (self._maxValue - self._minValue)
        return normalized_value * 100

    def _request_pin_value(self, pin):
        ser = serial.Serial(port=self._port, baudrate=self._baudrate, timeout=10)
        ser.flush()
        time.sleep(2)

        command = "ra %d\n" % pin
        ser.write(command.encode('ascii'))
        ser.flush()

        line = ser.readline().decode('ascii').strip()
        (pinType, pinNumber, valueString) = line.split(' ')

        if pinType != "analog" and int(pinNumber) != self._pin:
            return None

        return float(int(valueString)) / 1024.0
