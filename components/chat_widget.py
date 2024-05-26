import json
import rc_icons
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QApplication, QSizePolicy, \
    QTextEdit

from backend.main import get_response
#
# ai_icon = "icons/ai_icon.png"
# user_icon = "icons/user_icon.svg"


class GrowingTextEdit(QTextEdit):
    def __init__(self, *args, **kwargs):
        super(GrowingTextEdit, self).__init__(*args, **kwargs)
        self.setObjectName('main-label')
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Set the size policy to expand
        self.setReadOnly(True)

    def resizeEvent(self, event):
        super(GrowingTextEdit, self).resizeEvent(event)
        contents_height = self.document().size().height()
        self.setFixedHeight(contents_height)  # Adjust the height based on the contents and add padding


def clear_layout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()


def save_chat_history(chat_history):
    with open('chat_history.json', 'w') as file:
        json.dump(chat_history, file, indent=4)


def get_chat_history():
    try:
        with open('chat_history.json', 'r') as file:
            chat_history = json.load(file)
    except FileNotFoundError:
        chat_history = []
    return chat_history


def update_chat_history(prompt, response):
    chat_history = get_chat_history()
    if not chat_history or 'content' not in chat_history[-1]:
        chat_history.append({"chat_id": len(chat_history) + 1, "message": prompt, "content": []})
    elif not chat_history[-1]['content']:
        chat_history[-1]['message'] = prompt
    # Append the prompt and response as a dictionary to the 'content' list of the last chat
    chat_history[-1]['content'].append({"prompt": prompt, "response": response})
    save_chat_history(chat_history)


class ChatWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setObjectName('chat-widget')
        self.setMinimumWidth(500)
        self.setLayout(self.layout)

        self.response_widget = QWidget()
        self.response_widget.setObjectName('main-chat-widget')
        # self.response_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.response_layout = QVBoxLayout()
        # set alignment to top
        self.response_layout.setAlignment(Qt.Alignment.AlignTop)
        self.response_widget.setLayout(self.response_layout)

        # Create a QScrollArea and set the response_widget as its widget
        self.response_scroll_area = QScrollArea()
        self.response_scroll_area.setWidgetResizable(True)
        self.response_scroll_area.setWidget(self.response_widget)

        # Add the QScrollArea to the layout instead of the response_widget
        self.layout.addWidget(self.response_scroll_area)  # Add stretch factor to response_widget
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
        prompt_layout = QHBoxLayout()
        prompt_layout.setContentsMargins(0, 0, 0, 0)
        prompt_icon = QLabel()
        icon = QIcon(':/icons/user_icon.svg')  # Create QIcon from the SVG file
        pixmap = icon.pixmap(20, 20)  # Create QPixmap from QIcon
        prompt_icon.setPixmap(pixmap)  # Set QPixmap as the icon for QLabel
        prompt_icon.setFixedSize(20, 20)  # Set a fixed size for the icon

        prompt_label = GrowingTextEdit(prompt)
        prompt_label.setObjectName('prompt-label')
        prompt_label.setReadOnly(True)

        prompt_layout.addWidget(prompt_icon)
        prompt_layout.addWidget(prompt_label)
        prompt_layout.setAlignment(Qt.AlignTop)
        prompt_layout.setAlignment(prompt_icon, Qt.AlignTop)
        prompt_widget = QWidget()
        prompt_widget.setObjectName('prompt-widget')
        prompt_widget.setLayout(prompt_layout)
        self.response_layout.addWidget(prompt_widget)

        self.response_layout.setAlignment(prompt_widget, Qt.AlignTop)

    def response_widget_method(self, response):
        response_layout = QHBoxLayout()
        response_layout.setContentsMargins(0, 0, 0, 0)
        response_icon = QLabel()
        icon = QIcon(':/icons/ai_icon.png')  # Create QIcon from the SVG file
        pixmap = icon.pixmap(20, 20)  # Create QPixmap from QIcon
        response_icon.setPixmap(pixmap)  # Set QPixmap as the icon for QLabel
        response_icon.setFixedSize(20, 20)  # Set a fixed size for the icon
        response_label = GrowingTextEdit(response)
        response_label.setObjectName('response-label')
        response_label.setReadOnly(True)
        response_layout.addWidget(response_icon)
        response_layout.addWidget(response_label)  # Set a stretch factor for the response
        response_layout.setAlignment(Qt.AlignTop)  # Align the layout to the top
        response_layout.setAlignment(response_icon, Qt.AlignTop)
        response_widget = QWidget()
        response_widget.setObjectName('response-widget')
        response_widget.setLayout(response_layout)
        self.response_layout.addWidget(response_widget)
        self.response_layout.setAlignment(response_widget, Qt.AlignTop)

    def input_widget(self):
        input_widget = QWidget()
        input_layout = QHBoxLayout()
        input_field = QLineEdit()
        input_field.setObjectName('input-field')
        input_field.setPlaceholderText("Ask a question...")

        submit_button = QPushButton("")
        # Set the icon for the submit button
        icon = QIcon(":icons/send.svg")  # Path to the icon file
        submit_button.setIcon(icon)
        submit_button.setObjectName('submit-button')
        submit_button.setCursor(Qt.PointingHandCursor)

        submit_button.clicked.connect(self.submit_button_clicked)
        input_layout.addWidget(input_field)
        input_layout.addWidget(submit_button)
        input_widget.setLayout(input_layout)
        input_widget.setContentsMargins(0, 0, 0, 0)
        input_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.layout.addWidget(input_widget)
        input_widget.setObjectName('input-widget')
        return input_widget

    def get_input(self):
        input_widget = self.layout.itemAt(1).widget()
        input_field = input_widget.layout().itemAt(0).widget()
        return input_field.text().strip()

    def submit_button_clicked(self):
        input_text = self.get_input()
        # print(input_text)

        # Add a new prompt label with the text from the input field
        prompt_layout = QHBoxLayout()
        prompt_layout.setContentsMargins(0, 0, 0, 0)
        prompt_icon = QLabel()
        icon = QIcon(':/icons/user_icon.svg')  # Create QIcon from the SVG file
        pixmap = icon.pixmap(20, 20)  # Create QPixmap from QIcon
        prompt_icon.setPixmap(pixmap)  # Set QPixmap as the icon for QLabel
        prompt_icon.setFixedSize(20, 20)  # Set a fixed size for the icon

        prompt_label = GrowingTextEdit(input_text)
        prompt_label.setObjectName('prompt-label')
        prompt_label.setReadOnly(True)

        prompt_layout.addWidget(prompt_icon)
        prompt_layout.addWidget(prompt_label)  # Set a stretch factor for the prompt
        prompt_layout.setAlignment(Qt.AlignTop)  # Align the layout to the top
        prompt_layout.setAlignment(prompt_icon, Qt.AlignTop)
        prompt_widget = QWidget()
        prompt_widget.setObjectName('prompt-widget')
        prompt_widget.setLayout(prompt_layout)
        self.response_layout.addWidget(prompt_widget)
        self.response_layout.setAlignment(prompt_widget, Qt.AlignTop)

        # Add a new response label with the text "Answer goes here"
        response_layout = QHBoxLayout()
        response_layout.setContentsMargins(0, 0, 0, 0)
        response_icon = QLabel()
        icon = QIcon(':/icons/ai_icon.png')  # Create QIcon from the SVG file
        pixmap = icon.pixmap(20, 20)  # Create QPixmap from QIcon
        response_icon.setPixmap(pixmap)  # Set QPixmap as the icon for QLabel
        response_icon.setFixedSize(20, 20)  # Set a fixed size for the icon
        response_label = GrowingTextEdit()
        response_label.setObjectName('response-label')
        response_label.setReadOnly(True)
        response_layout.addWidget(response_icon)
        response_layout.addWidget(response_label)  # Set a stretch factor for the response
        response_layout.setAlignment(Qt.AlignTop)  # Align the layout to the top
        response_layout.setAlignment(response_icon, Qt.AlignTop)
        response_widget = QWidget()
        response_widget.setObjectName('response-widget')
        response_widget.setLayout(response_layout)
        self.response_layout.addWidget(response_widget)
        self.response_layout.setAlignment(response_widget, Qt.AlignTop)

        for chunk in get_response(input_text):
            lines = chunk.split('\n')  # Split the chunk into lines
            lines[0] = lines[0].lstrip('\n')  # Remove leading newline character from the first line
            chunk = '\n'.join(lines)  # Join the lines back together
            response_label.setText(response_label.toPlainText() + chunk)  # Append the chunk to the response text
            contents_height = response_label.document().size().height()
            response_label.setFixedHeight(contents_height+48)  # Adjust the height based on the contents and add padding
            QApplication.processEvents()
            # Force UI update after each chunk append
            # after each response append \n to the response label
        response_label.setText(response_label.toPlainText() )
        contents_height = response_label.document().size().height()
        response_label.setFixedHeight(contents_height+48)
        # after response complete update the chat history
        update_chat_history(input_text, response_label.toPlainText())
        self.clear_input()

    def clear_input(self):
        input_widget = self.layout.itemAt(1).widget()
        input_field = input_widget.layout().itemAt(0).widget()
        input_field.clear()
