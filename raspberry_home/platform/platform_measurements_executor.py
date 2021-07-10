from datetime import datetime
from typing import List

from raspberry_home.platform.measurement import Measurement
from raspberry_home.platform.measurements_scheduler import MeasurementsExecutor
from raspberry_home.platform.sensor import Sensor


class PlatformMeasurementsExecutor(MeasurementsExecutor):

    def __init__(self, sensors: [Sensor]):
        self.sensors = sensors

    def perform_measurements(self) -> List[Measurement]:
        print("Begin measurements...")
        measurements = []
        for sensor in self.sensors:
            for characteristic in sensor.get_characteristics():
                start_time = datetime.now()
                try:
                    value = sensor.get_value(characteristic)
                    end_time = datetime.now()

                    print("%s [PlatformMeasurementsExecutor]: {sensor: %s, characteristic: %s} value: %s (in %f ms)"
                          % (datetime.now().strftime("%H:%M:%S.%f"), sensor.name, characteristic.name,
                             sensor.formatted_value_with_unit(characteristic, value),
                             (end_time - start_time).total_seconds() * 1000.0))

                    measurement = Measurement(sensor, characteristic, value, start_time, end_time)
                    measurements.append(measurement)
                except Exception as error:
                    print("%s [PlatformMeasurementsExecutor]: {sensor: %s, characteristic: %s} Error: %s"
                          % (datetime.now().strftime("%H:%M:%S.%f"), sensor.name, characteristic.name, error))
        print("Finished measurements")
        return measurements
