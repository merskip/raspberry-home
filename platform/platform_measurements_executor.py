from datetime import datetime
from typing import List

from platform.measurement import Measurement
from platform.measurements_scheduler import MeasurementsExecutor
from platform.platform import Platform


class PlatformMeasurementsExecutor(MeasurementsExecutor):

    def __init__(self, platform: Platform):
        self.platform = platform

    def perform_measurements(self) -> List[Measurement]:
        measurements = []
        for sensor in self.platform.get_sensors():
            for characteristic in sensor.get_characteristics():
                start_time = datetime.now()
                value = sensor.get_value(characteristic)
                end_time = datetime.now()

                measurement = Measurement(sensor, characteristic, value, start_time, end_time)
                measurements.append(measurement)

        return measurements
