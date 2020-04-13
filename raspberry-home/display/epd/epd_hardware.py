import RPi.GPIO as GPIO
from time import sleep
import spidev


class EPDHardware:

    def __init__(self, spi_bus, spi_device,
                 reset_pin: int, dc_pin: int, cs_pin: int, busy_pin: int):
        self._reset_pin = reset_pin
        self._dc_pin = dc_pin
        self._cs_pin = cs_pin
        self._busy_pin = busy_pin
        self._spi = spidev.SpiDev(spi_bus, spi_device)

    def __del__(self):
        GPIO.cleanup([self._reset_pin, self._dc_pin, self._cs_pin, self._busy_pin])

    def setup(self):
        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BCM)

        for pin in [self._reset_pin, self._dc_pin, self._cs_pin]:
            GPIO.setup(pin, GPIO.OUT)

        for pin in [self._busy_pin]:
            GPIO.setup(pin, GPIO.IN)

        self._spi.max_speed_hz = 2000000
        self._spi.mode = 0

    def hard_reset(self):
        self._pin_write(self._reset_pin, GPIO.LOW)  # Turn off
        self._sleep(200)
        self._pin_write(self._reset_pin, GPIO.HIGH)  # Turn on
        self._sleep(200)

    def send(self, command: int, data: list = None):
        self.send_command(command)
        if data is not None:
            self.send_data(data)

    def send_command(self, command: int):
        self._pin_write(self._dc_pin, GPIO.LOW)
        self._spi_write([command])

    def send_data(self, data: list):
        self._pin_write(self._dc_pin, GPIO.HIGH)
        self._spi_write(data)

    def wait_until_idle(self):
        while self._pin_read(self._busy_pin) == 0:
            self._sleep(100)

    @staticmethod
    def _pin_write(pin, value: bool):
        GPIO.output(pin, value)

    @staticmethod
    def _pin_read(pin):
        return GPIO.input(pin)

    def _spi_write(self, data):
        # We've to send each byte by separated call `writebytes`
        for byte in data:
            self._spi.writebytes([byte])

    @staticmethod
    def divide_chunks(l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]

    @staticmethod
    def _sleep(milliseconds):
        sleep(milliseconds / 1000.0)
