class ChatWindow:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)

    def get_messages(self):
        return self.messages
