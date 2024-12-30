from flask_login import UserMixin
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    Username = Column(String, primary_key=True, nullable=False)
    Password = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(Username='{self.Username}', Password='{self.Password}')>"

    def to_dict(self):
        return {
            "Username": self.Username,
            "Password": self.Password
        }
