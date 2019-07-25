from platform.platform import Platform
from sensor.ds18b20 import DS18B20Sensor


class PlatformImpl(Platform):

    def __init__(self):
        super().__init__([
            DS18B20Sensor("Inside", "01186e6706ff"),
            DS18B20Sensor("Outside", "0114659b7dff"),
        ])
