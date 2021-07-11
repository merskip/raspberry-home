from raspberry_home.controller.chart_controller import ChartController
from raspberry_home.controller.home_controller import HomeController
from raspberry_home.controller.root_controller import RootController
from raspberry_home.controller.utils.moon import Moon
from raspberry_home.controller.utils.sun import Sun
from raspberry_home.open_weather_api import OpenWeatherApi
from raspberry_home.platform.measurements_scheduler import MeasurementsScheduler
from raspberry_home.platform.platform_measurements_executor import PlatformMeasurementsExecutor

from raspberry_home.view.renderable import Renderable


def run(is_simulator: bool):
    if is_simulator:
        Renderable.set_show_frames(True)

    if is_simulator:
        from raspberry_home.simulator.simulator_components_provider import SimulatorComponentsProvider
        components_provider = SimulatorComponentsProvider()
    else:
        from raspberry_home.board.board_components_provider import BoardComponentsProvider
        components_provider = BoardComponentsProvider()

    measurements_executor = PlatformMeasurementsExecutor(components_provider.get_sensors())

    time_intervals = components_provider.get_scheduler_time_intervals()
    measurement_scheduler = MeasurementsScheduler(time_intervals, measurements_executor)

    home_controller = HomeController(
        sun=Sun(
            coords={
                'longitude': 22.4937312,  # Lublin
                'latitude': 51.2181956
            },
            timezone_offset=7200  # UTC+2
        ),
        moon=Moon(),
        open_weather_api=OpenWeatherApi(
            city='Lublin',
            app_id='41e4c8c15e16553fddc1103361723979'
        )
    )

    chart_controller = ChartController()

    root_controller = RootController(
        display=components_provider.get_display(),
        screens=[
            home_controller,
            chart_controller
        ]
    )
    components_provider.get_input_controls().add_listener(root_controller)

    for measurements_listener in components_provider.get_measurements_listeners():
        measurement_scheduler.add_listener(measurements_listener)
    measurement_scheduler.add_listener(home_controller)
    measurement_scheduler.add_listener(root_controller)

    measurement_scheduler.begin_measurements_in_thread()
    components_provider.on_measurement_begin()
    if is_simulator:
        measurement_scheduler.stop_measurements()
    else:
        measurement_scheduler.wait_until_finish_measurements()
