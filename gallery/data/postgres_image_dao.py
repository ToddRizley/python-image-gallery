from gallery.data.db import *
from gallery.data.image import Image
from gallery.data.image_dao import ImageDAO
from gallery.aws.s3 import put_object, delete_object

class PostgresImageDAO(ImageDAO):

    def __init__(self):
        pass

    def get_images_for_username(self,username):
        result = []
        cursor = execute("SELECT id, file, owner FROM images WHERE owner=%s", (username,))
        for t in cursor.fetchall():
            result.append(Image(t[0], t[1], t[2]))
        #self.pull_user_images(bucket, result)
        return result

   # def pull_user_images(self,bucket,image_list):
   #     for image in image_list:
   #         file_path = f"gallery/ui/downloads/{image.file}"
   #         download_object(bucket, image.file, f"gallery/ui/downloads/{image.file.split('/')[0]}")
    
    def get_image_by_id_and_username(self, image_id, username):
        cursor = execute("SELECT id, file, owner FROM images WHERE id=%s AND owner=%s", (image_id, username))
        t = cursor.fetchone()
        result = Image(t[0], t[1], t[2])
        return result

    def delete_user_image(self, bucket, image):
        delete_object(bucket, image.file)
        res = execute("DELETE FROM images WHERE id=%s", (image.id_num,))
        return res

    def add_image(self, bucket, file_path, username, image_file):
        res = execute("INSERT INTO images (file, owner) VALUES (%s, %s)", (file_path, username))
        put_object(bucket, file_path, image_file)

        return res

