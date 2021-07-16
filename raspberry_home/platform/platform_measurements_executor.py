from time import sleep

from datetime import datetime
from typing import List, Optional

from raspberry_home.logger import Logger
from raspberry_home.platform.characteristic import Characteristic
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
                measurement = self._perform_measurement_for_characteristic(
                    sensor=sensor, characteristic=characteristic,
                    retry_count=5, retry_delay=2
                )
                if measurement is not None:
                    measurements.append(measurement)
                else:
                    self.logger.error("Failed perform measurement for sensor=%s, characteristic=%s"
                                      % (sensor.name, characteristic.name))
        return measurements

    def _perform_measurement_for_characteristic(self,
                                                sensor: Sensor,
                                                characteristic: Characteristic,
                                                retry_count: int,
                                                retry_delay: float) -> Optional[Measurement]:
        remaining_retry = retry_count
        while remaining_retry > 0:
            start_time = datetime.now()
            self.logger.start_timer()
            try:
                value = sensor.get_value(characteristic)
                if value is None:
                    raise Exception("the value is none")
                end_time = datetime.now()

                self.logger.info("sensor=%s, characteristic=%s, value=%s"
                                 % (sensor.name, characteristic.name,
                                    sensor.formatted_value_with_unit(characteristic, value)))

                return Measurement(sensor, characteristic, value, start_time, end_time)
            except Exception as error:
                remaining_retry -= 1
                self.logger.warning("sensor=%s, characteristic=%s (%d tries remaining)"
                                    % (sensor.name, characteristic.name, remaining_retry), error)
                if remaining_retry > 0:
                    sleep(retry_delay)
        return None
