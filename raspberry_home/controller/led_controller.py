from typing import List

from raspberry_home.controller.utils.led_output import LEDOutput
from raspberry_home.platform.measurement import Measurement
from raspberry_home.platform.measurements_scheduler import MeasurementsListener


class LEDController(MeasurementsListener):

    def __init__(self, led_output: LEDOutput):
        self.led_output = led_output

    def on_begin_measurements(self):
        self.led_output.turn_on()

    def on_measurements(self, measurements: List[Measurement]):
        self.led_output.turn_off()
