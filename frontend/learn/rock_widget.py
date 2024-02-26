from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout


def button_1_clicked():
    print("Button 1")


def button_2_clicked():
    print("Button 2")


class RockWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RockWidget")
        button_1 = QPushButton("Button 1")
        button_1.clicked.connect(button_1_clicked)
        button_2 = QPushButton("Button 2")
        button_2.clicked.connect(button_2_clicked)

        # button_layout = QHBoxLayout()
        button_layout = QVBoxLayout()
        button_layout.addWidget(button_1)
        button_layout.addWidget(button_2)

        self.setLayout(button_layout)

