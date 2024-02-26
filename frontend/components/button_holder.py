from PySide6.QtWidgets import QMainWindow, QPushButton





class ButtonHolder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Button Holder app")
        button = QPushButton("Press me")
        self.setCentralWidget(button)
