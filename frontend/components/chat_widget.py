from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
import json
from PySide6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout


def clear_layout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()


class ChatWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setObjectName('chat-widget')
        self.setMinimumWidth(500)
        self.setLayout(self.layout)

        self.response_widget = QWidget()
        self.response_widget.setObjectName('response-widget')
        self.response_layout = QVBoxLayout()
        self.response_widget.setLayout(self.response_layout)

        # Create a QScrollArea and set the response_widget as its widget
        self.response_scroll_area = QScrollArea()
        self.response_scroll_area.setWidgetResizable(True)
        self.response_scroll_area.setWidget(self.response_widget)

        # Add the QScrollArea to the layout instead of the response_widget
        self.layout.addWidget(self.response_scroll_area, stretch=1)  # Add stretch factor to response_widget
        self.input_widget = self.input_widget()
        self.input_widget.setEnabled(False)

        # chat_history = self.get_chat_history
        # if chat_history:
        #     self.changePage(chat_history[0])

    def changePage(self, chat_widget):
        chat_widget_data = json.loads(chat_widget)
        clear_layout(self.response_layout)
        for item in chat_widget_data['content']:
            self.prompt_widget(item['prompt'])
            self.response_widget_method(item["response"])
        self.input_widget.setEnabled(True)

    def prompt_widget(self, prompt):
        prompt_label = QLabel(prompt)
        self.response_layout.addWidget(prompt_label)
        self.response_layout.setAlignment(Qt.Alignment.AlignTop)

    def response_widget_method(self, response):  # change this line
        response_label = QLabel(response)
        self.response_layout.addWidget(response_label)
        self.response_layout.setAlignment(Qt.Alignment.AlignTop)

    def input_widget(self):
        input_widget = QWidget()
        input_layout = QHBoxLayout()
        input_field = QLineEdit()
        input_field.setPlaceholderText("Ask a question...")
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit_button_clicked)
        input_layout.addWidget(input_field)
        input_layout.addWidget(submit_button)
        input_widget.setLayout(input_layout)
        self.layout.addWidget(input_widget)
        input_widget.setObjectName('input-widget')
        return input_widget

    def get_input(self):
        input_widget = self.layout.itemAt(1).widget()
        input_field = input_widget.layout().itemAt(0).widget()
        return input_field.text().strip()

    def submit_button_clicked(self):
        input_text = self.get_input()
        print(input_text)
        self.clear_input()
    #      get res stream it in new res label
    #      after stream save the chat history
    #      remove the response widget with streamed response
    #      update the chat history widget from history

    def clear_input(self):
        input_widget = self.layout.itemAt(1).widget()
        input_field = input_widget.layout().itemAt(0).widget()
        input_field.clear()
