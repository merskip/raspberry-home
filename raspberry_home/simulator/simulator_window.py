from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QPushButton, QVBoxLayout
from pyqt_led import Led


class SimulatorWindow(QWidget):

    def __init__(self):
        super().__init__(flags=Qt.WindowFlags())
        self.setWindowTitle("Raspberry Home - Simulator")

        self.display_label = QLabel()
        self.display_label.setStyleSheet("border: 5px solid gray")
        self.led_output = Led(self, shape=Led.circle, on_color=Led.red)

        buttons_layout = QVBoxLayout()
        for i in range(0, 4):
            button = QPushButton("KEY%i" % (i + 1))
            buttons_layout.addWidget(button, alignment=Qt.AlignLeft)

        self.layout = QHBoxLayout()
        self.layout.addLayout(buttons_layout)
        self.layout.addWidget(self.display_label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.led_output, alignment=Qt.AlignTrailing)

        self.setLayout(self.layout)

    def set_display(self, image: QImage):
        self.display_label.setPixmap(QPixmap(image))

    def set_led_output(self, state: bool):
        self.led_output.turn_on(state)
