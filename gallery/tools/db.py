import psycopg2
import json
from .secrets import get_secret_image_gallery

connection = None

def get_secret():
    jsonString = get_secret_image_gallery()
    return json.loads(jsonString)

def connect():
    global connection
    secret = get_secret()
    connection = psycopg2.connect(host=secret['host'], dbname=secret['db_name'], user= secret['username'], password= secret['password'])
    connection.set_session(autocommit=True)

def execute(query, args=None):
    global connection
    cursor = connection.cursor()
    try:
        if not args:
            cursor.execute(query)
        else:
            cursor.execute(query, args)
        return cursor
    except Exception as e:
        print(e)
        return False

def add_user(username, password, full_name):
    res = execute("INSERT INTO users (username, password, full_name) VALUES (%s, %s, %s)", (username, password, full_name) )
    return res    
    
def get_user(username):
    res = execute("SELECT * FROM users WHERE username=%s", (username,))
    return res

def get_users():
    res = execute("SELECT * FROM users")
    return res

def edit_full_name(username, new_full_name):
    res = execute("UPDATE users SET full_name=%s where username=%s", (new_full_name, username))
    return res

def edit_password(username, new_password):
    res = execute("UPDATE users SET password=%s where username=%s", (new_password, username))
    return res
    
def delete_user(username):
    res = execute("DELETE FROM users WHERE username=%s", (username,))
    return res
