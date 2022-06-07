import psycopg2
import json
from gallery.aws.secrets import get_secret_image_gallery

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
