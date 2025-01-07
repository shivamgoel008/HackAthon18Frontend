from werkzeug.security import generate_password_hash, check_password_hash

from backend.database.user import UserRepository


class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def authenticate(self, username, password):
        user = self.user_repo.get_by_username(username)
        if user:
            return check_password_hash(user['password'], password)
        return False

    def create_new_user(self, data):
        user = self.user_repo.get_by_username(data['username'])
        if user:
            return {"error": "User already exists"}
        data['password'] = generate_password_hash(data['password'])
        user_id = self.user_repo.create_new_user(data)
        return {"message": f"User {user_id} created successfully"}