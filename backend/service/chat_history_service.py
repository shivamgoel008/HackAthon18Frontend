from database.chat_history import ChatHistoryRepository


class ChatHistoryService:
    def __init__(self):
        self.chat_history_repo = ChatHistoryRepository()

    def add_chat_message(self, data):
        return self.chat_history_repo.add_message(data["user_id"], data["chat_id"], data["message"])

    def get_messages_for_user_chat(self, user_id, chat_id):
        return self.chat_history_repo.get_messages(user_id, chat_id)

    def get_all_chats_for_user(self, user_id):
        return self.chat_history_repo.get_all_chats(user_id)

    def edit_message(self, user_id, chat_id, message_id, new_message):
        pass

    def delete_message(self, user_id, chat_id, message_id):
        pass