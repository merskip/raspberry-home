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

                print("%s [PlatformMeasurementsExecutor]: {sensor: %s, characteristic: %s} value: %s (in %f ms)"
                      % (datetime.now().strftime("%H:%M:%S.%f"), sensor.name, characteristic.name,
                         sensor.formatted_value_with_unit(characteristic, value),
                         (end_time - start_time).total_seconds() * 1000.0))

                measurement = Measurement(sensor, characteristic, value, start_time, end_time)
                measurements.append(measurement)

        return measurements
