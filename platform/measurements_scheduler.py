import time
from abc import ABC, abstractmethod
from typing import List

from platform.measurement import Measurement


class MeasurementsExecutor(ABC):

    @abstractmethod
    def perform_measurements(self) -> List[Measurement]:
        pass


class MeasurementsListener(ABC):

    @abstractmethod
    def on_measurements(self, measurements: List[Measurement]):
        pass


class MeasurementsScheduler:
    measurements_executor: MeasurementsExecutor
    listeners: List[MeasurementsListener]

    def __init__(self, measurements_executor: MeasurementsExecutor):
        self.listeners = []
        self.measurements_executor = measurements_executor

    def append(self, listener: MeasurementsListener):
        self.listeners.append(listener)

    def begin_measurements(self):
        import schedule
        schedule.every(5).minutes.do(self.perform_single_measurement)
        self.perform_single_measurement()

        while 1:
            schedule.run_pending()
            time.sleep(1)

    def perform_single_measurement(self):
        measurements = self.measurements_executor.perform_measurements()
        for listener in self.listeners:
            listener.on_measurements(measurements)
