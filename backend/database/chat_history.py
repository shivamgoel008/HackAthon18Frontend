from datetime import datetime
import traceback
from database.connection import DBConnection


class ChatHistoryRepository:
    def __init__(self):
        self.connection = DBConnection()
        self.client = self.connection.connect()
        self.db = self.client["Makeathon18"]
        self.collection = self.db["chat_history"]

    def add_message(self, user_id, chat_id, message_info):
        print(user_id, chat_id, message_info)
        try:
            with self.client.start_session() as session:
                with session.start_transaction():
                    chat = self.collection.find_one({"user_id": user_id, "chat_id": chat_id})
                    print(chat)
                    message_info["timestamp"] = datetime.now()
                    print(message_info)
                    if chat:
                        self.collection.update_one(
                            {"user_id": user_id, "chat_id": chat_id},
                            {"$push": {"messages": message_info}},
                        )
                    else:
                        new_chat = {
                            "user_id": user_id,
                            "chat_id": chat_id,
                            "messages": [message_info]
                        }
                        self.collection.insert_one(new_chat)
            return {"message": "Message added successfully"}
        except Exception:
            traceback.print_exc()
            raise Exception("Error while adding message")

    def get_messages(self, user_id, chat_id):
        chat = self.collection.find_one({"user_id": user_id, "chat_id": chat_id})
        if chat:
            return {"messages": chat.get("messages", [])}
        else:
            raise Exception("Chat not found")

    def get_all_chats(self, user_id):
        chats = self.collection.find({"user_id": user_id}, {"_id": 0, "user_id": 1, "chat_id": 1, "messages": 1}).to_list()
        if chats:
            return chats
        else:
            raise Exception("No chats found")

    def edit_message(self, user_id, chat_id, message_id, new_message):
        pass

    def delete_message(self, user_id, chat_id, message_id):
        pass

