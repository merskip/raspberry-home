from platform.platform import Platform
from platform.sensor import Characteristics
from stub.stub_sensor import StubSensor


class StubPlatform(Platform):

    def __init__(self):
        super().__init__([
            self._create_temperature_sensor(),
            self._create_light_sensor(),
            self._create_door_sensor(),
            self._create_pressure_sensor()
        ])

    @staticmethod
    def _create_temperature_sensor():
        return StubSensor("DS18B20",
                          [Characteristics.temperature],
                          lambda c: 24.5)

    @staticmethod
    def _create_light_sensor():
        return StubSensor("TSL2561",
                          [Characteristics.light],
                          lambda c: 250.23)

    @staticmethod
    def _create_door_sensor():
        return StubSensor("CMD14",
                          [Characteristics.boolean],
                          lambda c: True)

    @staticmethod
    def _create_pressure_sensor():
        def get_value(c):
            if c is Characteristics.temperature:
                return 25.0
            else:
                return 980.0

        return StubSensor("BMP180",
                          [Characteristics.temperature, Characteristics.pressure],
                          get_value)
