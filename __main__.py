import sys

from display.display import Display
from display.save_file_display import SaveFileDisplay
from controller.home_controller import HomeController
from platform.platform import Platform
from stub.stub_platform import StubPlatform

is_simulator_arg = len(sys.argv) > 1 and str(sys.argv[1]) == "simulator"


def get_platform() -> Platform:
    if is_simulator_arg:
        return StubPlatform()
    else:
        from platform_impl import PlatformImpl
        return PlatformImpl()


def get_display() -> Display:
    if is_simulator_arg:
        return SaveFileDisplay("result.bmp", (264, 176))
    else:
        from epd.epd2in7b_display import EPD2in7BDisplay
        return EPD2in7BDisplay()


def print_all_sensors_values():
    for sensor in platform.get_sensors():
        print("Sensor \"%s\" (%s):" % (sensor.name, sensor.__class__.__name__))
        for characteristic in sensor.get_characteristics():
            print(" - characteristic: %s" % characteristic.name)
            value = sensor.get_value_with_unit(characteristic)
            print("   value: %s" % value)


if __name__ == "__main__":
    platform = get_platform()

    print_all_sensors_values()

    display = get_display()
    display_controller = HomeController(platform, display)
    display_controller.refresh()
