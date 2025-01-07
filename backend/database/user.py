import traceback
from .connection import DBConnection


class UserRepository:
    def __init__(self):
        self.connection = DBConnection()
        self.client = self.connection.connect()
        self.db = self.client["Makeathon18"]
        self.collection = self.db["users"]

    def get_by_username(self, username):
        return self.collection.find_one({"username": username})

    def create_new_user(self, data: dict):
        try:
            with self.client.start_session() as s:
                with s.start_transaction():
                    user = {
                        "username": data["username"],
                        "password": data["password"]
                    }
                    user_id = self.collection.insert_one(user).inserted_id
                    return user_id
        except Exception:
            stack_trace = traceback.format_exc()
            return {"error": stack_trace}

    def check_connection_expiry(self):
        pass

    def authenticate(self, username, password):
        pass
