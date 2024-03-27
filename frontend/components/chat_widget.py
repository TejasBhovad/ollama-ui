from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QApplication, QSpacerItem, QSizePolicy
import json
from PySide6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout

from backend.main import get_response


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
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.response_layout.addItem(spacer)  # Add spacer at the beginning of the layout

        prompt_label = QLabel(prompt)
        prompt_label.setObjectName('prompt-label')
        prompt_label.setWordWrap(True)
        self.response_layout.addWidget(prompt_label)
        self.response_layout.setAlignment(Qt.Alignment.AlignTop)

    def response_widget_method(self, response):
        response_label = QLabel(response)
        response_label.setObjectName('response-label')
        response_label.setWordWrap(True)
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

        # Add a new prompt label with the text from the input field
        prompt_label = QLabel(input_text)
        prompt_label.setObjectName('prompt-label')
        prompt_label.setWordWrap(True)
        prompt_label.adjustSize()
        self.response_layout.addWidget(prompt_label)
        self.response_layout.setAlignment(Qt.Alignment.AlignTop)

        # Add a new response label with the text "Answer goes here"
        response_label = QLabel()
        response_label.setObjectName('response-label')
        response_label.setWordWrap(True)
        self.response_layout.addWidget(response_label)
        self.response_layout.setAlignment(Qt.Alignment.AlignTop)

        for chunk in get_response(input_text):
            response_label.setText(response_label.text() + chunk)
            QApplication.processEvents()
            # Force UI update after each chunk append
            # after each response append \n to the response label
        response_label.setText(response_label.text() + "\n")
        response_label.adjustSize()
        # after response complete update the chat history
        update_chat_history(input_text, response_label.text())
        self.clear_input()

    #      get res stream it in new res label
    #      after stream save the chat history
    #      remove the response widget with streamed response
    #      update the chat history widget from history

    def clear_input(self):
        input_widget = self.layout.itemAt(1).widget()
        input_field = input_widget.layout().itemAt(0).widget()
        input_field.clear()
