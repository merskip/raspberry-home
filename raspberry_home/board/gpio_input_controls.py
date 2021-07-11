from time import sleep

from raspberry_home.controller.input_controls import InputControls

import RPi.GPIO as GPIO


class GPIOInputControls(InputControls):

    pins = [5, 6, 13, 19]

    def __init__(self):
        super().__init__()
        for pin in self.pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin, GPIO.RISING, callback=self._detected_pin_changed, bouncetime=200)

    def _detected_pin_changed(self, channel):
        button_index = self.pins.index(channel)
        self._notify_listener_clicked_button(button_index)
