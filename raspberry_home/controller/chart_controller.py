from typing import List

from raspberry_home.database.sqllite_repository import SqliteRepository
from raspberry_home.platform.measurement import Measurement
from raspberry_home.platform.sensor import Sensor
from raspberry_home.view.line_chart import LineChart, LineChartSeries
from raspberry_home.view.text import Text
from raspberry_home.view.view import View
from raspberry_home.view.widget import Widget


class ChartController(Widget):

    def __init__(self, repository: SqliteRepository, sensors: List[Sensor]):
        self.repository = repository
        self.sensors = sensors

    def build(self) -> View:
        series: List[LineChartSeries] = []

        for sensor in self.sensors:
            for characteristic in sensor.get_characteristics():
                measurements = self.repository.get_measurements(sensor, characteristic)

                points = list(map(lambda m: (m.time_start.timestamp(), m.value), measurements))
                series.append(LineChartSeries(
                    points=points
                ))

        return LineChart(
            series=series
        )
