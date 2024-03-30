import json
import rc_icons
from PySide6.QtCore import Qt, Signal, QFileSystemWatcher, QSize
from PySide6.QtGui import QCursor, QIcon
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel


class ClickableWidget(QWidget):
    clicked = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("ClickableWidget")

    def mousePressEvent(self, event):
        self.clicked.emit()


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

        # Create a QFileSystemWatcher and add the chat_history file to it
        self.file_watcher = QFileSystemWatcher()
        self.file_watcher.addPath(self.history_file)
        self.file_watcher.fileChanged.connect(self.on_file_changed)

        new_chat_button = QPushButton(" New Chat")
        new_chat_button.setMaximumWidth(self.maximumWidth())
        new_chat_button.setObjectName("new-chat-button")
        new_chat_button.setCursor(QCursor(Qt.PointingHandCursor))
        new_chat_button.setAttribute(Qt.WA_StyledBackground, True)
        plus_icon = QIcon(":/icons/plus.svg")  # Path to the icon file
        new_chat_button.setIcon(plus_icon)
        new_chat_button.setIconSize(QSize(14, 14))
        # align center
        new_chat_button.setStyleSheet("text-align: center;")

        self.history_widget = QWidget()
        self.history_widget.setMaximumWidth(self.maximumWidth())
        self.history_widget.setObjectName("history-widget")
        history_layout = QVBoxLayout()
        history_layout.setContentsMargins(2, 7.5, 2, 0)

        # Add QLabel in history layout saying history
        history_label = QLabel("HISTORY")
        history_label.setObjectName("history-label")
        # remove margin from history label
        history_label.setContentsMargins(4, 15, 2, 0)
        # set max height for history label
        history_label.setMaximumHeight(27)

        history_layout.setAlignment(Qt.Alignment.AlignTop)

        self.history_widget.setLayout(history_layout)
        sidebar_layout = QVBoxLayout()
        sidebar_layout.addWidget(new_chat_button)
        sidebar_layout.addWidget(history_label)
        sidebar_layout.addWidget(self.history_widget)
        self.setLayout(sidebar_layout)

        new_chat_button.clicked.connect(
            lambda: self.addChatToHistoryAndEmitSignal("New Chat Session"))
        self.updateHistoryWidget()

    def on_file_changed(self, path):
        # When the chat_history file changes, reload the chat history and update the history widget
        if path == self.history_file:
            self.loadChatHistory()
            self.updateHistoryWidget()

    def newButton(self, text="Button", chat_message=None):
        if chat_message is None:
            content = []
        button = QPushButton(self)
        button.setObjectName("chat-button")
        button.setText(text)
        button.setStyleSheet("text-align: left;")
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
        # print("Adding chat to history")
        self.chat_history.append({"chat_id": len(self.chat_history) + 1, "message": message, "content": []})
        # print(self.chat_history)
        self.updateHistoryWidget()
        self.saveChatHistory()

    def addChatToHistoryAndEmitSignal(self, message="template message"):
        # print("Adding chat to history")
        new_chat = {"chat_id": len(self.chat_history) + 1, "message": message, "content": []}
        self.chat_history.append(new_chat)
        # print(self.chat_history)
        self.updateHistoryWidget()
        self.saveChatHistory()
        self.page_content.emit(json.dumps(new_chat))  # Emit the signal with the new chat session

    def updateHistoryWidget(self):

        # clear the layout first
        for i in reversed(range(self.history_widget.layout().count())):
            self.history_widget.layout().itemAt(i).widget().setParent(None)

        for chat_message in self.chat_history:
            # Create a new widget for each chat message
            message_widget = ClickableWidget()
            message_widget.setAttribute(Qt.WA_StyledBackground, True)
            message_widget.clicked.connect(
                lambda chat=chat_message: self.sendSignal(chat))
            message_layout = QHBoxLayout()
            message_widget.setLayout(message_layout)
            message_widget.setObjectName("message-widget")
            message_widget.setCursor(QCursor(Qt.PointingHandCursor))
            message_layout.setContentsMargins(0, 0, 0, 0)

            # Create the chat button
            chat_button = self.newButton(chat_message["message"], chat_message)
            message_layout.addWidget(chat_button, stretch=1)

            # Create the delete button
            delete_button = QPushButton("")
            delete_button.setCursor(QCursor(Qt.PointingHandCursor))
            delete_button.setIcon(QIcon(":/icons/trash.svg"))
            delete_button.setObjectName("delete-button")
            delete_button.setMaximumWidth(24)
            delete_button.clicked.connect(lambda: self.deleteChatMessage(chat_message))
            message_layout.addWidget(delete_button)

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

    def sendSignal(self, chat_message):
        # print("Sending signal", chat_message)
        self.page_content.emit(json.dumps(chat_message))
