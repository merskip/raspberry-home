from datetime import datetime
from typing import List

from raspberry_home.logger import Logger
from raspberry_home.platform.measurement import Measurement
from raspberry_home.platform.measurements_scheduler import MeasurementsExecutor
from raspberry_home.platform.sensor import Sensor


class PlatformMeasurementsExecutor(MeasurementsExecutor):
    logger = Logger("PlatformMeasurementsExecutor")

    def __init__(self, sensors: [Sensor]):
        self.sensors = sensors

    def perform_measurements(self) -> List[Measurement]:
        measurements = []
        for sensor in self.sensors:
            for characteristic in sensor.get_characteristics():
                start_time = datetime.now()
                self.logger.start_timer()
                try:
                    value = sensor.get_value(characteristic)
                    end_time = datetime.now()

                    self.logger.info("sensor=%s, characteristic=%s, value=%s"
                                     % (sensor.name, characteristic.name,
                                        sensor.formatted_value_with_unit(characteristic, value)))

                    measurement = Measurement(sensor, characteristic, value, start_time, end_time)
                    measurements.append(measurement)
                except Exception as error:
                    self.logger.error("sensor=%s, characteristic=%s" % (sensor.name, characteristic.name), error)
        return measurements
