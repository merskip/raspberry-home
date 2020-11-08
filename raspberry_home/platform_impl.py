from raspberry_home.platform.platform import Platform
from raspberry_home.sensor.bh1750sensor import BH1750Sensor
from raspberry_home.sensor.bmp180sensor import BMP180Sensor
from raspberry_home.sensor.covid19monitor import COVID19Monitor
from raspberry_home.sensor.ds18b20sensor import DS18B20Sensor
from raspberry_home.sensor.soilmoisturesensor import SoilMoistureSensor


class PlatformImpl(Platform):

    def __init__(self):
        super().__init__([
            DS18B20Sensor(1, "DS18B20 Inside", "01186e6706ff"),
            DS18B20Sensor(2, "DS18B20 Outside", "0114659b7dff").with_flag("outside"),
            BMP180Sensor(3, "BMP180", 0x77, 1.029850746268657),
            BH1750Sensor(4, "BH1750", 0x23),
            # SoilMoistureSensor(5, "Right flower", "/dev/ttyACM0", 9600, pin=0),
            COVID19Monitor(6, "COVID19-Poland", "poland"),
        ])
