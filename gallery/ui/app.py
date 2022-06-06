from flask import Flask, request, render_template, url_for, redirect, session
from gallery.tools.db import connect, get_users, get_user, add_user, edit_full_name, edit_password, delete_user
#from gallery.tools.user import User
#from gallery.tools.postgres_user_dao import PostgresUserDAO
from gallery.tools.secrets import get_secret_flask_session
app = Flask(__name__)
app.secret_key = get_secret_flask_session()

connect()

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_exec', methods=['POST'])
def login_exec():
    user = get_user(request.form['username']).fetchone()
    ## Update method to use DAO/user class
    if user is None or user[1] != request.form['password']:
        return redirect('/invalid_login')
    else:
        session["username"] = user[0]
        return redirect("/admin")
    
@app.route('/invalid_login')
def invalid_login():
    ##message flash redirect to /login
    return render_template('invalid_login.html')

@app.route('/admin')
def admin():
    users = get_users()
    return render_template('admin.html', users=prepare_user_list(users))

@app.route('/admin/add_new_user')
def add_new_user():
    return render_template("add_new_user.html")

@app.route('/admin/create_user', methods=['POST'])
def create_user():

    username = request.form['username']
    full_name = request.form['full_name']
    password = request.form['password']
    add_user(username, password, full_name)

    return  redirect('/admin')

@app.route('/admin/deletion_confirmation/<username>', methods=['GET'])
def deletion_confirmation(username):
    return render_template("deletion_confirmation.html", username=username)

@app.route('/admin/delete_user/<username>', methods=['POST'])
def delete_user_route(username):
    delete_user(username)

    return  redirect('/admin')

@app.route('/admin/edit_user/<username>', methods=['GET'])
def edit_user(username):
    
    row = get_user(username).fetchone()
    user = {'username': row[0], 'password': row[1], 'full_name': row[2]}
    return render_template("edit_user.html", user=user)

@app.route('/admin/update_user/<username>', methods=['POST'])
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

# @app.route('/hello')
# def hello():
#    return '<p>hello world!</p>'

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
