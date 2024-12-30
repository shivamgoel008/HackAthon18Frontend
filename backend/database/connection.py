import os
from sqlalchemy import create_engine, MetaData
from .tables.user import Base
from dotenv import load_dotenv
from .db_authentication import DBAuthentication

load_dotenv()


class DBConnection:
    server = os.environ.get('DB_CONNECTION_URL')
    database = os.environ.get('DATABASE_NAME')

    def __init__(self):
        self.connection_string = f'{self.server}/{self.database}'

    def connect(self):
        # auth_token = DBAuthentication.generate_token()
        return create_engine(url=self.connection_string)
