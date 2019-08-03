from platform.characteristic import Characteristics
from platform.platform import Platform
from stub.stub_sensor import StubSensor


class StubPlatform(Platform):

    def __init__(self):
        super().__init__([
            self._create_temperature_sensor(),
            self._create_temperature_outside_sensor(),
            self._create_light_sensor(),
            self._create_door_sensor(),
            self._create_pressure_sensor()
        ])

    @staticmethod
    def _create_temperature_sensor():
        return StubSensor(
            1, "DS18B20",
            [Characteristics.temperature],
            lambda c: 24.5
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
            [Characteristics.light],
            lambda c: 250.23
        )

    @staticmethod
    def _create_door_sensor():
        return StubSensor(
            4, "CMD14",
            [Characteristics.boolean],
            lambda c: True
        ).with_flag("door")

    @staticmethod
    def _create_pressure_sensor():
        return StubSensor(
            5, "BMP180",
            [Characteristics.pressure, Characteristics.temperature],
            lambda c: 25.0 if c is Characteristics.temperature else 980.0
        )
