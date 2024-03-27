import json

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout


class Sidebar(QWidget):
    page_content = Signal(str)

    def __init__(self):
        super().__init__()

        self.chat_history = []
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
            lambda: self.addChatToHistory("New Chat new"))
        self.updateHistoryWidget()

    def newButton(self, text="Button", chat_message=None):
        if chat_message is None:
            content = []
        button = QPushButton(self)
        button.setObjectName("chat-button")
        button.setText(text)
        # print idx when button is clicked
        # button.clicked.connect(lambda x: print("Button clicked: ", idx))
        button.clicked.connect(lambda x: self.page_content.emit(json.dumps(chat_message)))
        return button

    def loadChatHistory(self):
        try:
            with open(self.history_file, 'r') as file:
                self.chat_history = json.load(file)
        except FileNotFoundError:
            self.saveChatHistory()

    def saveChatHistory(self):
        with open(self.history_file, 'w') as file:
            json.dump(self.chat_history, file)

    def addChatToHistory(self, message="template message"):
        print("Adding chat to history")
        self.chat_history.append({"chat_id": len(self.chat_history) + 1, "message": message, "content": []})
        print(self.chat_history)
        self.updateHistoryWidget()
        self.saveChatHistory()

    def updateHistoryWidget(self):
        # clear the layout first
        for i in reversed(range(self.history_widget.layout().count())):
            self.history_widget.layout().itemAt(i).widget().setParent(None)

        for chat_message in self.chat_history:
            # Create a new widget for each chat message
            message_widget = QWidget()
            message_layout = QHBoxLayout()
            message_widget.setLayout(message_layout)
            message_widget.setObjectName("message-widget")

            # Create the chat button
            chat_button = self.newButton(chat_message["message"], chat_message)
            message_layout.addWidget(chat_button, stretch=2)

            # Create the delete button
            delete_button = QPushButton("-")
            delete_button.setObjectName("delete-button")
            delete_button.setMaximumWidth(24)
            delete_button.clicked.connect(lambda: self.deleteChatMessage(chat_message))
            message_layout.addWidget(delete_button, stretch=1)

            # Add the message widget to the history widget
            self.history_widget.layout().addWidget(message_widget)

        self.history_widget.setLayout(self.history_widget.layout())

    def deleteChatMessage(self, chat_message):
        # Remove the chat message from the chat history
        self.chat_history.remove(chat_message)
        # remove the chat message from json file
        self.saveChatHistory()

        # Update the history widget
        self.updateHistoryWidget()
