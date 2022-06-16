from gallery.data.db import *
from gallery.data.image import Image
from gallery.data.image_dao import ImageDAO
from gallery.aws.s3 import put_object, get_object

class PostgresImageDAO(ImageDAO):

    def __init__(self):
        pass

    def get_images_for_username(self,bucket,username):
        result = []
        cursor = execute("SELECT id, file, owner FROM images WHERE owner=%s", (username,))
        for t in cursor.fetchall():
            result.append(Image(t[0], t[1], t[2]))
        data = pull_user_images(bucket, result)
        return data

    def pull_user_images(self,bucket,image_list):
        result_set = []
        for image in image_list:
            result_set.append(get_object(bucket, image.file))
        return result_set
            
    def add_image(self, bucket, file_path, username, image_file):
        res = execute("INSERT INTO images (file, owner) VALUES (%s, %s)", (file_path, username))
        put_object(bucket, file_path, image_file)

        return res

