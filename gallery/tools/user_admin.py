import db

db_instance = None
def main():
    global db_instance 
    db_instance = db.DBConnector()
    db_instance.set_db_vars(host_in = "demo-db-1.c0dnixzhpyd9.us-east-1.rds.amazonaws.com",
     name_in= "image_gallery", 
     user_in= "image_gallery", 
     password_file_in= "/home/ec2-user/.image_gallery_config")
    db_instance.connect()

    do_continue = True
    while do_continue is True:
        selection = int(get_menu_selection())
        if selection in range(1,6, 1):
            if selection == 1:
                list_users()
            elif selection == 2:
                add_user()
            elif selection == 3:
                edit_user()
            elif selection == 4:
                delete_user()
            elif selection == 5:
                do_continue = quit_prog()
        else:
            print("\nInvalid command. Please selection again\n")
            do_continue = True

def get_menu_selection():
    print("\nChoose an action: \n")
    print("1) List users \n2) Add user\n3) Edit user\n4) Delete user\n5) Quit\n")
    print("Enter command> ")

    return input().strip()

def delete_user():
    global db_instance
    print("\nEnter username to delete> ")
    u_name = input().strip()
    print(f"\nAre you sure that you want to delete {u_name}?")
    confirmation = input().strip().lower()
    
    if confirmation == 'y' or confirmation == 'yes':
        res = db_instance.delete_user(u_name)
        if not res:
            print("No such user.")
        print("Deleted.")

def edit_user():
    global db_instance
    print("\nUsername to edit> ")
    u_name = input().strip()

    if not u_name:
        print("\nNo such user.")
        return

    print("\nNew password (press enter to keep current)> ")
    p_word = input().strip()
    if p_word:
        res = db_instance.edit_password(u_name, p_word)
        if not res:
            print("An error occurred.")

    print("\nNew full name (press enter to keep current)> ")
    f_name = input().strip()
    
    if f_name:
      res = db_instance.edit_full_name(u_name, f_name)
      if not res:
            print("An error occurred.")

def list_users():
    global db_instance

    print("\nusername\tpassword\tfull name")
    print("-----------------------------------------\n")
    res = db_instance.get_users()
    for row in res:
        print(row[0]+"\t\t"+row[1]+"\t\t"+row[2])
         
def add_user():
    global db_instance
    print("\nUsername> ")
    u_name = input().strip()
    print("\nPassword> ")
    p_word = input().strip()
    print("\nFull name> ")
    f_name = input().strip()
    res = db_instance.add_user(u_name, p_word, f_name)
    if not res:
        print("An error occurred.")
        print(res)

def quit_prog():
    print("\nBye.")
    return False
    
if __name__ == '__main__':
    main() 
