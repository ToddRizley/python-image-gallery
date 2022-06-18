from gallery.data.db import *
from gallery.data.user import User
from gallery.data.user_dao import UserDAO

class PostgresUserDAO(UserDAO):

    def __init__(self):
        pass

    def get_users(self):
        result = []
        cursor = execute("SELECT username, password, full_name, is_admin FROM users")
        for t in cursor.fetchall():
            result.append(User(t[0], t[1], t[2], t[3]))
        return result

    def add_user(self, username, password, full_name, is_admin):
        res = execute("INSERT INTO users (username, password, full_name, is_admin) VALUES (%s, %s, %s, %s)", (username, password, full_name, is_admin))
        return res    
    
    def get_user(self, username):
        row = execute("SELECT * FROM users WHERE username=%s", (username,)).fetchone()
        if row is None:
            return None
        else:
            return User(row[0], row[1], row[2], row[3])

    def edit_full_name(self, username, new_full_name):
        res = execute("UPDATE users SET full_name=%s where username=%s", (new_full_name, username))
        return res

    def edit_password(self, username, new_password):
        res = execute("UPDATE users SET password=%s where username=%s", (new_password, username))
        return res
    
    def delete_user(self, username):
        res = execute("DELETE FROM users WHERE username=%s", (username,))
        return res

#    def get_images_for_username(self, username):
#        result = []
#        cursor = execute("SELECT id, file, owner FROM images WHERE owner=%s", (username,))
#        for t in cursor.fetchall():
#            result.append(Image(t[0], t[1], t[2]))
#        return result
