from typing import List, Callable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QCheckBox
from pyqt_led import Led

from raspberry_home.view.renderable import Renderable


class SimulatorWindow(QWidget):

    def __init__(self):
        super().__init__(flags=Qt.WindowFlags())
        self.setWindowTitle("Raspberry Home - Simulator")

        buttons_layout = QVBoxLayout()
        self.buttons: List[QPushButton] = []
        for i in range(0, 4):
            button = QPushButton("KEY %i" % (i + 1), self)
            buttons_layout.addWidget(button, alignment=Qt.AlignLeft)
            self.buttons.append(button)

        self.display_label = QLabel(self)
        self.display_label.setStyleSheet("border: 5px solid gray")

        right_layout = QVBoxLayout()

        self.led_output = Led(self, shape=Led.circle, on_color=Led.red)

        self.frames_check_box = QCheckBox("Frames", self)
        self.frames_check_box.setChecked(Renderable.is_show_frames)

        right_layout.addWidget(self.frames_check_box, alignment=Qt.AlignTrailing)
        right_layout.addWidget(self.led_output, alignment=Qt.AlignCenter)

        self.layout = QHBoxLayout()
        self.layout.addLayout(buttons_layout)
        self.layout.addWidget(self.display_label, alignment=Qt.AlignCenter)
        self.layout.addLayout(right_layout)

        self.setLayout(self.layout)

    def set_display(self, image: QImage):
        self.display_label.setPixmap(QPixmap(image))

    def set_led_output(self, state: bool):
        self.led_output.turn_on(state)
