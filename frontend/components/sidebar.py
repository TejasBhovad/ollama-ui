from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton


class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("sidebar")

        self.setMaximumWidth(250)
        self.setMinimumWidth(200)

        button = QPushButton("Button")
        button.setMaximumWidth(self.maximumWidth())
        button.setStyleSheet("background-color: green; color: white")

        history = QWidget()
        history.setMaximumWidth(self.maximumWidth())
        history.setStyleSheet("background-color: blue")

        layout = QVBoxLayout()
        layout.addWidget(button)
        layout.addWidget(history)
        self.setLayout(layout)
