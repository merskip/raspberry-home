from raspberry_home.platform.characteristic import Characteristics
from raspberry_home.platform.platform import Platform
from raspberry_home.sensor.covid19monitor import COVID19Monitor
from raspberry_home.stub.stub_sensor import StubSensor


class StubPlatform(Platform):

    def __init__(self):
        super().__init__([
            self._create_temperature_sensor(),
            self._create_temperature_outside_sensor(),
            self._create_light_sensor(),
            self._create_pressure_sensor(),
            self._create_door_sensor(),
            COVID19Monitor(7, "COVID19-Poland", "poland")
        ])

    @staticmethod
    def _create_temperature_sensor():
        return StubSensor(
            1, "DS18B20",
            [Characteristics.temperature.set(min_value=0, accuracy=0.5)],
            lambda c: 24.33
        )

    @staticmethod
    def _create_temperature_outside_sensor():
        return StubSensor(
            2, "DS18B20 Outside",
            [Characteristics.temperature],
            lambda c: 30.5
        ).with_flag("outside")

    @staticmethod
    def _create_light_sensor():
        return StubSensor(
            3, "TSL2561",
            [Characteristics.light.set(min_value=1.0, accuracy=1.0)],
            lambda c: 250.23
        )

    @staticmethod
    def _create_door_sensor():
        return StubSensor(
            5, "CMD14",
            [Characteristics.boolean],
            lambda c: True
        ).with_flag("door")

    @staticmethod
    def _create_pressure_sensor():
        return StubSensor(
            6, "BMP180",
            [Characteristics.pressure.set(accuracy=0.1), Characteristics.temperature],
            lambda c: 25.0 if c is Characteristics.temperature else 980.0 * 1.029850746268657
        )
