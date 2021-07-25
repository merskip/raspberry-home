from typing import List

from raspberry_home.database.sqllite_repository import SqliteRepository
from raspberry_home.platform.sensor import Sensor
from raspberry_home.view.chart import ChartLine
from raspberry_home.view.text import Text
from raspberry_home.view.view import View
from raspberry_home.view.widget import Widget


class ChartController(Widget):

    def __init__(self, repository: SqliteRepository, sensors: List[Sensor]):
        self.repository = repository
        self.sensors = sensors

    def build(self) -> View:
        children = []

        for sensor in self.sensors:
            for characteristic in sensor.get_characteristics():
                measurements = self.repository.get_measurements(sensor, characteristic)
                children += [
                    Text("Sensor[%s.%s]" % (sensor.name, characteristic.name)),
                    Text("m=%s" % list(map(lambda m: m.value, measurements)))
                ]

        return ChartLine(
            points=[(0.0, 0.0), (0.2, 0.4), (0.3, 0.3), (0.4, 0.6), (1.0, 1.0)],
        )
