from PySide6.QtWidgets import QLineEdit


class InputField:
    def __init__(self):
        self.input_field = QLineEdit()

    def get_input(self):
        return self.input_field.text().strip()

    def clear(self):
        self.input_field.clear()
