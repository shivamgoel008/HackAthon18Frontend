import os
import traceback
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from .tables.user import User
from .connection import DBConnection


class UserRepository:
    def __init__(self):
        self.refresh_connection()
        # time when connection refresh last
        self.last_refreshed_at = datetime.now()
        # refresh time in seconds
        self.refresh_time = int(os.environ.get('DB_TOKEN_REFRESH_TIME'))

    def refresh_connection(self):
        self.connection = DBConnection()
        self.engine = self.connection.connect()
        self.session = sessionmaker(bind=self.engine)()
        self.last_refreshed_at = datetime.now()

    def get_by_username(self, username):
        if self.check_connection_expiry():
            self.refresh_connection()
        return self.session.query(User).filter(User.Username == username).first()

    def create_new_user(self, data: dict):
        try:
            user = User(Username=data['username'], Password=data['password'])
            self.session.add(user)
            self.session.commit()
            return {"message": "User created successfully"}
        except Exception:
            self.session.rollback()
            stack_trace = traceback.format_exc()
            return {"error": stack_trace}

    def check_connection_expiry(self):
        pass

    def authenticate(self, username, password):
        pass
