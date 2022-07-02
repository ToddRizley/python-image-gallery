import psycopg2, os, json
from gallery.aws.secrets import get_secret_image_gallery

connection = None

def get_secret():
    jsonString = get_secret_image_gallery()
    return json.loads(jsonString)

def connect():
    global connection
#    secret = get_secret()
#    connection = psycopg2.connect(host=secret['host'], dbname=secret['db_name'], user= secret['username'], password= secret['password'])
    ig_password  = open(os.getenv("IG_PASSWD_FILE"), "r").readline().strip()

    connection = psycopg2.connect(host= os.getenv("PG_HOST"), port=os.getenv("PG_PORT"),  dbname=os.getenv("IG_DATABASE"), user=os.getenv("IG_USER"), password=ig_password)
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
