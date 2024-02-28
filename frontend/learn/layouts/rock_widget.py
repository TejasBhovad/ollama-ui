from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox


def button_1_clicked():
    message = QMessageBox()
    message.setMinimumSize(700, 200)
    message.setWindowTitle("Title of message")
    message.setText('Something went wrong')
    message.setInformativeText("Choice is yours?")
    message.setIcon(QMessageBox.Warning)
    message.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    message.setDefaultButton(QMessageBox.Ok)

    ret = message.exec()
    if ret == QMessageBox.Ok:
        print("User chose Ok")
    else:
        print("User chose Cancel")
    print("Button 1")


def button_2_clicked(self):
    ret = QMessageBox.information(self, "Message title", "Some info", QMessageBox.Ok | QMessageBox.Cancel)
    if ret == QMessageBox.Ok:
        print("User chose Ok")
    else:
        print("User chose Cancel")
    print("Button 2")


class RockWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RockWidget")
        button_1 = QPushButton("Button 1")
        button_1.clicked.connect(button_1_clicked)
        button_2 = QPushButton("Button 2")
        button_2.clicked.connect(lambda: button_2_clicked(self))  # Lambda expression

        # button_layout = QHBoxLayout()
        button_layout = QVBoxLayout()
        button_layout.addWidget(button_1)
        button_layout.addWidget(button_2)

        self.setLayout(button_layout)
