import sys

from PyQt5.QtWidgets import QApplication

from raspberry_home.controller.utils.font import Font, FontWeight
from raspberry_home.test_window import TestWindow
#
#
# def get_platform(is_simulator) -> Platform:
#     if is_simulator:
#         return StubPlatform()
#     else:
#         from raspberry_home.platform_impl import PlatformImpl
#         return PlatformImpl()
#
#
# def print_all_sensors_values(platform: Platform):
#     for sensor in platform.get_sensors():
#         print("Sensor \"%s\" (%s):" % (sensor.name, sensor.__class__.__name__))
#         for characteristic in sensor.get_characteristics():
#             print(" - characteristic: %s" % characteristic.name)
#             value = sensor.get_value_with_unit(characteristic)
#             print("   value: %s" % value)
#
#
# def get_display(is_simulator, is_gui, simulator_window) -> Display:
#     if is_simulator:
#         if is_gui:
#             from raspberry_home.simulator.simulator_display import SimulatorDisplay
#             return SimulatorDisplay((264, 176), simulator_window)
#         else:
#             return SaveFileDisplay("result", (264, 176))
#     else:
#         from raspberry_home.display.epd.epd2in7_display import EPD2in7Display
#         return EPD2in7Display()
#
#
# def run(is_simulator: bool, is_gui: bool):
#     platform = get_platform(is_simulator)
#     if is_simulator:
#         print_all_sensors_values(platform)
#         from raspberry_home.simulator.simulator_window import SimulatorWindow
#         simulator_window = SimulatorWindow()
#     else:
#         simulator_window = None
#
#     display = get_display(is_simulator, is_gui, simulator_window)
#     home_controller = HomeController(
#         display,
#         coordinates={'longitude': 22.4937312, 'latitude': 51.2181956},  # Lublin
#         timezone_offset=7200  # UTC+2
#     )
#
#     measurements_executor = PlatformMeasurementsExecutor(platform)
#     measurement_scheduler = MeasurementsScheduler(int(config["scheduler"]["every_minutes"]), measurements_executor)
#     measurement_scheduler.append(home_controller)
#
#     if not is_simulator:
#         from raspberry_home.database.DatabaseWriter import DatabaseWriter
#         from sqlalchemy import create_engine
#         database_engine = create_engine(config["database"]["url"])
#         database_writer = DatabaseWriter(database_engine, platform)
#         measurement_scheduler.append(database_writer)
#
#
#     if is_simulator:
#         if is_gui:
#             from PyQt5.QtWidgets import QApplication
#             app = QApplication([])
#
#             from raspberry_home.simulator.simulator_led_output import SimulatorLEDOutput
#             from raspberry_home.simulator.simulator_display import SimulatorDisplay
#             from raspberry_home.simulator.simulator_input_controls import SimulatorInputControls
#
#             led_controller = LEDController(SimulatorLEDOutput(simulator_window))
#             measurement_scheduler.append(led_controller)
#
#             chart_controller = ChartController(display)
#
#             input_controls = SimulatorInputControls(simulator_window)
#             input_controller = InputController([home_controller, chart_controller])
#             input_controls.add_listener(input_controller)
#
#             measurement_scheduler.begin_measurements_in_thread()
#             simulator_window.show()
#             app.exec()
#             measurement_scheduler.stop_measurements()
#         else:
#             measurement_scheduler.stop_measurements()
#     else:
#         measurement_scheduler.begin_measurements_in_thread()
#
#     measurement_scheduler.wait_until_finish_measurements()
#
#
from raspberry_home.view.padding import Padding
from raspberry_home.view.renderable import Renderable
from raspberry_home.view.stack import VerticalStack, StackDistribution, StackAlignment, HorizontalStack
from raspberry_home.view.text import Text


def run(is_simulator: bool):
    if is_simulator:
        Renderable.set_show_bounds(True)

    view = Padding(
        padding=16,
        child=VerticalStack(
            spacing=8,
            distribution=StackDistribution.EqualSpacing,
            alignment=StackAlignment.Center,
            children=[
                Text("Hello world! Witaj Świecie.\nAaańŚ"),
                HorizontalStack(
                    spacing=4,
                    distribution=StackDistribution.Start,
                    alignment=StackAlignment.Start,
                    children=[
                        Text("123", font=Font(36, FontWeight.BOLD)),
                        Text("45"),
                        Text("567"),
                    ]
                ),
                Padding(
                    padding=24,
                    child=HorizontalStack(
                        spacing=4,
                        distribution=StackDistribution.EqualSpacing,
                        alignment=StackAlignment.Center,
                        children=[
                            Text("123"),
                            Text("45"),
                            Text("567", font=Font(36, FontWeight.BOLD)),
                        ]
                    )
                ),
                HorizontalStack(
                    spacing=4,
                    distribution=StackDistribution.Start,
                    alignment=StackAlignment.End,
                    children=[
                        Text("123"),
                        Text("45"),
                        Text("567", font=Font(36, FontWeight.BOLD)),
                    ]
                )
            ]
        )
    )

    app = QApplication(sys.argv)
    window = TestWindow(
        root_view=view
    )
    window.show()
    app.exec()

    # if is_simulator:
    #     from raspberry_home.simulator.simulator_components_provider import SimulatorComponentsProvider
    #     components_provider = SimulatorComponentsProvider()
    # else:
    #     from raspberry_home.board_components_provider import BoardComponentsProvider
    #     components_provider = BoardComponentsProvider()
    #
    # measurements_executor = PlatformMeasurementsExecutor(components_provider.get_sensors())
    #
    # time_intervals = components_provider.get_scheduler_time_intervals()
    # measurement_scheduler = MeasurementsScheduler(time_intervals, measurements_executor)
    #
    # display = components_provider.get_display()
    #
    # home_controller = HomeController(
    #     display=display,
    #     coordinates={'longitude': 22.4937312, 'latitude': 51.2181956},  # Lublin
    #     timezone_offset=7200  # UTC+2
    # )
    #
    # for measurements_listener in components_provider.get_measurements_listeners():
    #     measurement_scheduler.append(measurements_listener)
    # measurement_scheduler.append(home_controller)
    #
    # measurement_scheduler.begin_measurements_in_thread()
    # components_provider.on_measurement_begin()
    # measurement_scheduler.wait_until_finish_measurements()
