import sys
from configparser import ConfigParser

from raspberry_home.controller.home_controller import HomeController
from raspberry_home.display.save_file_display import SaveFileDisplay
from raspberry_home.display.display import Display
from raspberry_home.platform.measurements_scheduler import MeasurementsScheduler
from raspberry_home.platform.platform_measurements_executor import PlatformMeasurementsExecutor
from raspberry_home.stub.stub_platform import StubPlatform
from raspberry_home.platform.platform import Platform


def read_config():
    parser = ConfigParser()
    if not parser.read("config.ini"):
        raise RuntimeError("Failed read config file: config.ini")
    return parser


config = read_config()


def get_platform(is_simulator) -> Platform:
    if is_simulator:
        return StubPlatform()
    else:
        from raspberry_home.platform_impl import PlatformImpl
        return PlatformImpl()


def print_all_sensors_values(platform: Platform):
    for sensor in platform.get_sensors():
        print("Sensor \"%s\" (%s):" % (sensor.name, sensor.__class__.__name__))
        for characteristic in sensor.get_characteristics():
            print(" - characteristic: %s" % characteristic.name)
            value = sensor.get_value_with_unit(characteristic)
            print("   value: %s" % value)


def get_display(is_simulator) -> Display:
    if is_simulator:
        return SaveFileDisplay("result", (264, 176))
    else:
        from raspberry_home.display.epd.epd2in7_display import EPD2in7Display
        return EPD2in7Display()


def run_simulator():
    run(True)


def run(is_simulator: bool):
    platform = get_platform(is_simulator)
    if is_simulator:
        print_all_sensors_values(platform)

    display = get_display(is_simulator)
    home_controller = HomeController(
        display,
        coordinates={'longitude': 22.4937312, 'latitude': 51.2181956},  # Lublin
        timezone_offset=7200  # UTC+2
    )

    measurements_executor = PlatformMeasurementsExecutor(platform)
    measurement_scheduler = MeasurementsScheduler(int(config["scheduler"]["every_minutes"]), measurements_executor)
    measurement_scheduler.append(home_controller)

    if not is_simulator:
        from raspberry_home.database.DatabaseWriter import DatabaseWriter
        from sqlalchemy import create_engine
        database_engine = create_engine(config["database"]["url"])
        database_writer = DatabaseWriter(database_engine, platform)
        measurement_scheduler.append(database_writer)

    if is_simulator:
        measurement_scheduler.perform_single_measurement()
    else:
        measurement_scheduler.begin_measurements()


if __name__ == "__main__":
    run(is_simulator="--simulator" in sys.argv)
