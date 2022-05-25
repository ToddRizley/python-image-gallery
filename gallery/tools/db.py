import psycopg2


class DBConnector:

    def __init__(self):
        self.connection = None
        self.db_host = None
        self.db_name = None
        self.db_user = None
        self.password_file = None
    
    def set_db_vars(self, host_in, name_in, user_in, password_file_in):
        self.db_host = host_in
        self.db_name = name_in
        self.db_user = user_in
        self.password_file = password_file_in
        
    def get_password(self):
        f = open(self.password_file, "r")
        result = f.readline()
        f.close
        return result[:-1]

    def connect(self):
        self.connection = psycopg2.connect(host=self.db_host, dbname=self.db_name, user= self.db_user, password= self.get_password())

    def execute(self, query, args=None):
        cursor = self.connection.cursor()
        try:
            if not args:
                cursor.execute(query)
            else:
                cursor.execute(query, args)
            return cursor
        except Exception as e:
            print(e)
            return False

    def add_user(self, username, password, full_name):
        res = self.execute("INSERT INTO users (username, password, full_name) VALUES (%s, %s, %s)", (username, password, full_name) )
        return res

    def get_users(self):
        res = self.execute("SELECT * FROM users")
        return res

    def edit_full_name(self, username, new_full_name):
        res = self.execute("UPDATE users SET full_name=%s where username=%s", (new_full_name, username))
        return res

    def edit_password(self, username, new_password):
        res = self.execute("UPDATE users SET password=%s where username=%s", (new_password, username))
        return res
    
    def delete_user(self, username):
        print(username)
        res = self.execute("DELETE FROM users WHERE username=%s", (username,))
        return res

# def main():
#     connect()
#     res = execute("update users set password=%s where username='fred'", ('banana',))
#     res = execute('select * from users;')
#     for row in res:
#         print(row)

# if __name__ == '__main__':
#     main()

