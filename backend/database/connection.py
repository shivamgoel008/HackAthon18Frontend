import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


class DBConnection:
    def __init__(self):
        self.connection_string = os.environ.get("DB_URI")

    def connect(self):
        return MongoClient(self.connection_string)