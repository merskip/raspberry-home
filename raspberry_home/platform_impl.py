from raspberry_home.platform.platform import Platform
from raspberry_home.sensor.bh1750sensor import BH1750Sensor
from raspberry_home.sensor.bmp180sensor import BMP180Sensor
from raspberry_home.sensor.ds18b20sensor import DS18B20Sensor
from raspberry_home.sensor.dth22sensor import DTH22Sensor


class PlatformImpl(Platform):

    def __init__(self):
        super().__init__([
            DS18B20Sensor(id=1, name="DS18B20 Inside", device_id="01186e6706ff"),
            DS18B20Sensor(id=2, name="DS18B20 Outside", device_id="0114659b7dff").with_flag("outside"),
            BMP180Sensor(id=3, name="BMP180", address=0x77, pressure_factor=1.029850746268657),
            BH1750Sensor(id=4, name="BH1750", address=0x23),
            DTH22Sensor(id=5, name="DHT22", pin=27),
        ])
