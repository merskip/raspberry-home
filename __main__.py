import sys

from sqlalchemy import engine, create_engine

from controller.home_controller import HomeController
from display.display import Display
from display.save_file_display import SaveFileDisplay
from platform.measurements_scheduler import MeasurementsScheduler
from platform.platform import Platform
from platform.platform_measurements_executor import PlatformMeasurementsExecutor
from stub.stub_platform import StubPlatform

is_simulator = len(sys.argv) > 1 and str(sys.argv[1]) == "simulator"


def get_platform() -> Platform:
    if is_simulator:
        return StubPlatform()
    else:
        from platform_impl import PlatformImpl
        return PlatformImpl()


def get_display() -> Display:
    if is_simulator:
        return SaveFileDisplay("result.bmp", (264, 176))
    else:
        from epd.epd2in7b_display import EPD2in7BDisplay
        return EPD2in7BDisplay()


def get_database_engine() -> engine:
    if is_simulator:
        return create_engine('sqlite:///:memory:', echo=True)
    else:
        raise RuntimeError("Not implemented yet")


def print_all_sensors_values():
    for sensor in platform.get_sensors():
        print("Sensor \"%s\" (%s):" % (sensor.name, sensor.__class__.__name__))
        for characteristic in sensor.get_characteristics():
            print(" - characteristic: %s" % characteristic.name)
            value = sensor.get_value_with_unit(characteristic)
            print("   value: %s" % value)


if __name__ == "__main__":
    platform = get_platform()
    if is_simulator:
        print_all_sensors_values()

    # engine = get_database_engine()
    # Session = sessionmaker(bind=engine)
    # session = Session()
    #
    # Base.metadata.create_all(engine)
    #
    # session.add(Measurement(characteristic="temperature", value="12.0", formatted_value="12.0 *C"))
    # session.add(Measurement(characteristic="temperature", value="232.0", formatted_value="1232.0 *C"))
    #
    # measurements = session.query(Measurement).all()

    display = get_display()
    home_controller = HomeController(display)

    measurements_executor = PlatformMeasurementsExecutor(platform)
    measurement_scheduler = MeasurementsScheduler(measurements_executor)
    measurement_scheduler.append(home_controller)

    if is_simulator:
        measurement_scheduler.perform_single_measurement()
    else:
        measurement_scheduler.begin_measurements()
