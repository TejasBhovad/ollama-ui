from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
import json


class ChatWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setObjectName('chat-widget')
        self.setMinimumWidth(500)
        self.setLayout(self.layout)

        self.chat_area = QWidget()
        self.chat_area.setObjectName('chat-area')
        self.chat_area_layout = QVBoxLayout()
        self.chat_area.setLayout(self.chat_area_layout)
        self.layout.addWidget(self.chat_area)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def changePage(self, chat_widget):
        chat_widget_data = json.loads(chat_widget)
        self.clear_layout(self.chat_area_layout)
        for item in chat_widget_data['content']:
            self.prompt_widget(item['prompt'])
            self.response_widget(item['response'])

    def prompt_widget(self, prompt):
        prompt_label = QLabel(prompt)
        self.chat_area_layout.addWidget(prompt_label)
        self.chat_area_layout.setAlignment(Qt.Alignment.AlignTop)

    def response_widget(self, response):
        response_label = QLabel(response)
        self.chat_area_layout.addWidget(response_label)
        self.chat_area_layout.setAlignment(Qt.Alignment.AlignTop)