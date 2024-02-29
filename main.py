import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel
from frontend.components.input_field import InputField
from backend.main import get_response
from backend.logger import Logger
from PySide6.QtCore import Qt


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ollama UI")

        # Chat window layout (75% height)
        chat_window_layout = QVBoxLayout()
        chat_window_layout.setContentsMargins(0, 0, 0, 0)
        chat_window_layout.setSpacing(0)

        self.question_label = QLabel()
        self.question_label.setText("")
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignTop)
        self.question_label.setStyleSheet("margin: 0 1px; padding: 0;")  # Set minimal margins and no padding
        chat_window_layout.addWidget(self.question_label)

        # Response label with text wrapping and minimal margins/padding
        self.response_label = QLabel()
        self.response_label.setText("")
        self.response_label.setWordWrap(True)
        self.response_label.setAlignment(Qt.AlignTop)
        self.response_label.setStyleSheet("margin: 0 1px; padding: 0;")  # Set minimal margins and no padding
        chat_window_layout.addWidget(self.response_label )

        # Input window layout (25% height)
        input_window_layout = QHBoxLayout()  # Use QHBoxLayout for side-by-side elements
        input_window_layout.setContentsMargins(0, 0, 0, 0)
        input_window_layout.setSpacing(0)

        # add input field and button
        input_field = InputField()
        input_window_layout.addWidget(input_field.input_field)

        input_field.input_field.setPlaceholderText("Type your message here")

        # on button press log the input and clear the input field
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(lambda: Logger().log_user_input(input_field.get_input()))
        input_window_layout.addWidget(submit_button)
        submit_button.clicked.connect(
            lambda: submit_button_clicked(input_field, self.response_label, self.question_label))

        # on button press get response and log the response
        # submit_button.clicked.connect(lambda: Logger().log_response(get_response(input_field.get_input())))

        # Combine layouts in outer layout
        outerLayout = QVBoxLayout()
        outerLayout.addLayout(chat_window_layout, 5)  # Set stretch factor for 75%
        outerLayout.addLayout(input_window_layout, 1)  # Set stretch factor for 25%

        # Set the window's main layout
        self.setLayout(outerLayout)


def submit_button_clicked(input_field, response_label, question_label):
    # Prepend the user's question to the question label
    question_label.setText(input_field.get_input())
    for chunk in get_response(input_field.get_input()):
        response_label.setText(response_label.text() + chunk)
        app.processEvents()  # Force UI update after each chunk append
    # after each response append \n to the response label
    response_label.setText(response_label.text() + "\n")
    # log the response
    Logger().log_response(response_label.text())
    # Clear the input field and print
    input_field.clear()
    print("Button clicked")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
