import RPi.GPIO as GPIO

from raspberry_home.controller.led_output import LEDOutput


class GPIOLEDOutput(LEDOutput):

    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW)

    def __del__(self):
        GPIO.cleanup([self.pin])

    def turn_on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def turn_off(self):
        GPIO.output(self.pin, GPIO.LOW)
