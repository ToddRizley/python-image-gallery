from flask import Flask, request, render_template, url_for, redirect
from gallery.tools.db import connect, get_users, get_user, add_user, edit_full_name, edit_password, delete_user
#from gallery.tools.user import User
#from gallery.tools.postgres_user_dao import PostgresUserDAO

app = Flask(__name__)
connect()

@app.route('/admin')
def admin():
    users = get_users()
    return render_template('admin.html', users=prepare_user_list(users))

@app.route('/admin/add_new_user')
def add_new_user():
    return render_template("add_new_user.html")

@app.route('/create_user', methods=['POST'])
def create_user():

    username = request.form['username']
    full_name = request.form['full_name']
    password = request.form['password']
    add_user(username, password, full_name)

    return  redirect('/admin')

@app.route('/admin/deletion_confirmation/<username>', methods=['GET'])
def deletion_confirmation(username):
    return render_template("deletion_confirmation.html", username=username)

@app.route('/delete_user/<username>', methods=['POST'])
def delete_user_route(username):
    delete_user(username)

    return  redirect('/admin')

@app.route('/admin/edit_user/<username>', methods=['GET'])
def edit_user(username):
    
    row = get_user(username).fetchone()
    user = {'username': row[0], 'password': row[1], 'full_name': row[2]}
    return render_template("edit_user.html", user=user)

@app.route('/update_user/<username>', methods=['POST'])
def update_user(username):
    full_name = request.form['full_name']
    password = request.form['password']
    
    row = get_user(username).fetchone()
    user = {'username': row[0], 'password': row[1], 'full_name': row[2]}

    if user['password'] != password:
        edit_password(username, password)
    if user['full_name'] != full_name:
        edit_full_name(username, full_name)

    return  redirect('/admin')

@app.route('/hello')
def hello():
    return '<p>hello world!</p>'

#@app.route('/users')
#def users():
#    result = ""
#    for user in get_user_DAO().get_users():
#        result+= str(user.username)
#    return result
    

#Helper methods
#def get_user_DAO():
#    return PostgresUserDAO()

def prepare_user_list(users_object):
    result = []
    for row in users_object:
        result.append({'username': row[0], 'full_name':row[2]})
    return result
