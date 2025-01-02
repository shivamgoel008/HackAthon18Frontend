import traceback
from .connection import DBConnection


class UserRepository:
    def __init__(self):
        self.connection = DBConnection()
        self.client = self.connection.connect()
        self.db = self.client["Makeathon18"]
        self.collection = self.db["users"]

    def get_by_username(self, username):
        return self.collection.find({"username": username})

    def create_new_user(self, data: dict):
        try:
            with self.client.start_session() as s:
                s.start_transaction()
                user = {
                    "username": data["username"],
                    "password": data["password"]
                }
                user_id = self.collection.insert_one(user).inserted_id
                s.commit_transaction()
                return {"message": f"User {user_id} created successfully"}
        except Exception:
            stack_trace = traceback.format_exc()
            return {"error": stack_trace}

    def check_connection_expiry(self):
        pass

    def authenticate(self, username, password):
        pass
