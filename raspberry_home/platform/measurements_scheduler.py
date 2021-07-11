import threading
import time
from abc import ABC, abstractmethod
from typing import List

import schedule

from raspberry_home.platform.measurement import Measurement


class MeasurementsExecutor(ABC):

    @abstractmethod
    def perform_measurements(self) -> List[Measurement]:
        pass


class MeasurementsListener(ABC):

    def on_begin_measurements(self):
        pass

    def on_measurements(self, measurements: List[Measurement]):
        pass


class MeasurementsScheduler:
    active = False
    # listeners: List[MeasurementsListener]

    def __init__(self, time_intervals: int, measurements_executor: MeasurementsExecutor):
        self.thread = threading.Thread(target=self.begin_measurements, name='measuring-thread')
        self.listeners = []
        self.time_intervals = time_intervals
        self.measurements_executor = measurements_executor

    def append(self, listener: MeasurementsListener):
        self.listeners.append(listener)

    def begin_measurements_in_thread(self):
        self.active = True
        self.thread.start()

    def wait_until_finish_measurements(self):
        try:
            self.thread.join()
        except KeyboardInterrupt:
            pass

    def stop_measurements(self):
        self.active = False

    def begin_measurements(self):
        schedule.every(self.time_intervals).seconds.do(self._perform_single_measurement)
        self._perform_single_measurement()

        while self.active:
            schedule.run_pending()
            time.sleep(1)

    def _perform_single_measurement(self):
        self._notify_on_begin_measurements()
        measurements = self.measurements_executor.perform_measurements()
        self._notify_on_measurements(measurements)

    def _notify_on_begin_measurements(self):
        for listener in self.listeners:
            listener.on_begin_measurements()

    def _notify_on_measurements(self, measurements):
        for listener in self.listeners:
            listener.on_measurements(measurements)
