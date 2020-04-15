from raspberry_home.controller.led_output import LEDOutput
from raspberry_home.simulator.simulator_window import SimulatorWindow


class SimulatorLEDOutput(LEDOutput):

    def __init__(self, simulator_window: SimulatorWindow):
        self.simulator_window = simulator_window

    def turn_on(self):
        self.simulator_window.set_led_output(True)

    def turn_off(self):
        self.simulator_window.set_led_output(False)
