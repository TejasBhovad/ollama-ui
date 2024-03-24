import json

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout


class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("sidebar")

        self.setMaximumWidth(250)
        self.setMinimumWidth(200)

        self.history_file = "chat_history.json"
        self.loadChatHistory()

        new_chat_button = QPushButton("New Chat")
        new_chat_button.setMaximumWidth(self.maximumWidth())
        new_chat_button.setObjectName("new-chat-button")

        self.history_widget = QWidget()
        self.history_widget.setMaximumWidth(self.maximumWidth())
        self.history_widget.setObjectName("history-widget")
        history_layout = QVBoxLayout()
        history_layout.setAlignment(Qt.Alignment.AlignTop)
        self.history_widget.setLayout(history_layout)

        sidebar_layout = QVBoxLayout()
        sidebar_layout.addWidget(new_chat_button)
        sidebar_layout.addWidget(self.history_widget)
        self.setLayout(sidebar_layout)

        new_chat_button.clicked.connect(
            lambda: self.addChatToHistory("New Chat new"))  # Connect button click to lambda function
        self.updateHistoryWidget()

    def loadChatHistory(self):
        try:
            with open(self.history_file, 'r') as file:
                self.chat_history = json.load(file)
        except FileNotFoundError:
            self.chat_history = [
                {
                    "chat_id": 1,
                    "message": "Hello",
                },
                {
                    "chat_id": 2,
                    "message": "World",
                },
            ]
            self.saveChatHistory()

    def saveChatHistory(self):
        with open(self.history_file, 'w') as file:
            json.dump(self.chat_history, file)

    def addChatToHistory(self, message="template message"):
        print("Adding chat to history")
        self.chat_history.append({"chat_id": len(self.chat_history) + 1, "message": message})
        print(self.chat_history)
        self.updateHistoryWidget()
        self.saveChatHistory()

    def updateHistoryWidget(self):
        # clear the layout first
        for i in reversed(range(self.history_widget.layout().count())):
            self.history_widget.layout().itemAt(i).widget().setParent(None)

        for chat_message in self.chat_history:
            label = QLabel(chat_message["message"])
            self.history_widget.layout().addWidget(label)
        self.history_widget.setLayout(self.history_widget.layout())