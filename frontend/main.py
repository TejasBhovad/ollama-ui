import sys

from PySide6.QtWidgets import QApplication, QPushButton, QSlider
from PySide6.QtCore import Qt

app = QApplication(sys.argv)


def button_clicked(data):
    print("clicked", data)


def respond_to_slider(data):
    print("Percent: ", data)


button = QPushButton("Press me")
button.setCheckable(True)
button.clicked.connect(button_clicked)
# button.show()

slider = QSlider(Qt.Horizontal)
slider.setMinimum(1)
slider.setMaximum(100)
slider.setValue(25)
slider.valueChanged.connect(respond_to_slider)
slider.show()

# window = ButtonHolder()
# window.show()
app.exec()
