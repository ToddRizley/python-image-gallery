class User:

    def __init__(self, username, password, full_name, is_admin):
        self.username = username
        self.password = password
        self.full_name = full_name
        self.is_admin = is_admin

    def __repr__(self):
        return "Username: " + self.username + " password: " + self.password + " full name: " + self.full_name
