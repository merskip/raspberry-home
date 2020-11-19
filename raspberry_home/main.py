from raspberry_home.controller.home_controller import HomeController
from raspberry_home.platform.measurements_scheduler import MeasurementsScheduler
from raspberry_home.platform.platform_measurements_executor import PlatformMeasurementsExecutor

from raspberry_home.view.renderable import Renderable


def run(is_simulator: bool):
    if is_simulator:
        Renderable.set_show_bounds(True)

    if is_simulator:
        from raspberry_home.simulator.simulator_components_provider import SimulatorComponentsProvider
        components_provider = SimulatorComponentsProvider()
    else:
        from raspberry_home.board_components_provider import BoardComponentsProvider
        components_provider = BoardComponentsProvider()

    measurements_executor = PlatformMeasurementsExecutor(components_provider.get_sensors())

    time_intervals = components_provider.get_scheduler_time_intervals()
    measurement_scheduler = MeasurementsScheduler(time_intervals, measurements_executor)

    display = components_provider.get_display()

    home_controller = HomeController(
        display=display,
        coordinates={'longitude': 22.4937312, 'latitude': 51.2181956},  # Lublin
        timezone_offset=7200  # UTC+2
    )

    for measurements_listener in components_provider.get_measurements_listeners():
        measurement_scheduler.append(measurements_listener)
    measurement_scheduler.append(home_controller)

    measurement_scheduler.begin_measurements_in_thread()
    components_provider.on_measurement_begin()
    measurement_scheduler.wait_until_finish_measurements()
