import os
import sys

from PySide6.QtCore import Qt, QFileSystemWatcher
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout
from components.chat_widget import ChatWidget
from components.sidebar import Sidebar

# Set DEV_MODE to True for live update, False for no live update
DEV_MODE = True


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ollama UI")
        self.setWindowIcon(QIcon(':/icons/ai_icon.png'))
        self.setObjectName("window")
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        sidebar = Sidebar()
        sidebar.setAttribute(Qt.WA_StyledBackground, True)
        chat = ChatWidget()
        chat.setAttribute(Qt.WA_StyledBackground, True)

        layout.addWidget(sidebar, stretch=1)
        layout.addWidget(chat)
        self.setLayout(layout)
        self.resize(800, 600)
        sidebar.page_content.connect(chat.changePage)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    stylesheet_path = os.path.join(os.path.dirname(__file__), 'index.css')
    if os.path.exists(stylesheet_path):
        with open(stylesheet_path, 'r') as file:
            stylesheet = file.read()
            app.setStyleSheet(stylesheet)

    if DEV_MODE:
        watcher = QFileSystemWatcher()
        watcher.addPath('index.css')


        def update_stylesheet(path):
            new_stylesheet = open(path).read()
            app.setStyleSheet(new_stylesheet)

        watcher.fileChanged.connect(update_stylesheet)

    window = Window()
    window.show()
    sys.exit(app.exec())
