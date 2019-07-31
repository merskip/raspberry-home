from platform.platform import Platform
from platform.sensor import SpecificType
from sensor.bh1750sensor import BH1750Sensor
from sensor.bmp180sensor import BMP180Sensor
from sensor.ds18b20sensor import DS18B20Sensor
from sensor.dth11sensor import DTH11Sensor
from sensor.gpiosensor import GPIOSensor


class PlatformImpl(Platform):

    def __init__(self):
        super().__init__([
            DS18B20Sensor("DS18B20 Inside", "01186e6706ff"),
            DS18B20Sensor("DS18B20 Outside", "0114659b7dff", is_outside=True),
            BMP180Sensor("BMP180", 0x77),
            BH1750Sensor("BH1750", 0x23),
            DTH11Sensor("DTH11", 27),
            GPIOSensor("Balcony", 23, specific_type=SpecificType.boolean_door),
        ])
