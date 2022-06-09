from gallery.data.db import *
from gallery.data.image import Image
from gallery.data.image_dao import ImageDAO

class PostgresImageDAO(ImageDAO):

    def __init__(self):
        pass

    def get_images_for_username(self, username):
        result = []
        cursor = execute("SELECT id, file, owner FROM images WHERE owner=%s", (username,))
        for t in cursor.fetchall():
            result.append(Image(t[0], t[1], t[2]))
        return result

    def add_image(self, file, username):
        res = execute("INSERT INTO imagess (file, owner) VALUES (%s, %s)", (file, username))
        return res

