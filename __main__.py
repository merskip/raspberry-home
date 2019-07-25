import sys
from platform.platform import Platform
from platform.sensor import Characteristic
from stub.stub_platform import StubPlatform


def get_platform() -> Platform:
    is_simulator_arg = len(sys.argv) > 1 and str(sys.argv[1]) == "simulator"
    if is_simulator_arg:
        return StubPlatform()
    else:
        from platform_impl import PlatformImpl
        return PlatformImpl()


def format_value(value, characteristic: Characteristic) -> str:
    if characteristic.unit is not None:
        return "%s %s" % (value, characteristic.unit)
    else:
        return str(value)


if __name__ == "__main__":
    platform = get_platform()
    for sensor in platform.get_sensors():
        print("Sensor \"%s\" (%s):" % (sensor.name, sensor.__class__.__name__))
        for characteristic in sensor.get_characteristics():
            print(" - characteristic: %s" % characteristic.name)
            value = sensor.get_value(characteristic)
            print("   value: %s" % format_value(value, characteristic))
