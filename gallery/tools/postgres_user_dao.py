
from .db import *
from .user import User
from .user_dao import UserDAO

class PostgresUserDAO(UserDAO):

    def __init__(self):
        pass

    def get_users(self):
        result = []
        db_instance = DBConnector()
        db_instance.connect()
        cursor = db_instance.execute("SELECT username, password, full_name FROM users")
        for t in cursor.fetchall():
            result.append(User(t[0], t[1], t[2]))
        return result
