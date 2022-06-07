from flask import Flask, request, render_template, redirect, session
from gallery.data.db import connect
from gallery.data.user import User
from gallery.data.postgres_user_dao import PostgresUserDAO
from gallery.aws.secrets import get_secret_flask_session
from functools import wraps

app = Flask(__name__)
app.secret_key = get_secret_flask_session()

connect()

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_exec', methods=['POST'])
def login_exec():
    user = get_user_dao().get_user(request.form['username'])
    if user is None or user.password != request.form['password']:
        return redirect('/invalid_login')
    else:
        session["username"] = user.username
        return redirect("/admin")
    
@app.route('/invalid_login')
def invalid_login():
    ##message flash redirect to /login
    return render_template('invalid_login.html')

@app.route('/admin')
def admin():
    return render_template('admin.html', users= get_user_dao().get_users())

@app.route('/admin/add_new_user')
def add_new_user():
    return render_template("add_new_user.html")

@app.route('/admin/create_user', methods=['POST'])
def create_user():
    get_user_dao().add_user(request.form['username'], request.form['password'], request.form['full_name'])
    return  redirect('/admin')

@app.route('/admin/deletion_confirmation/<username>', methods=['GET'])
def deletion_confirmation(username):
    return render_template("deletion_confirmation.html", username=username)

@app.route('/admin/delete_user/<username>', methods=['POST'])
def delete_user_route(username):
    get_user_dao().delete_user(username)
    return  redirect('/admin')

@app.route('/admin/edit_user/<username>', methods=['GET'])
def edit_user(username):
    return render_template("edit_user.html", user= get_user_dao().get_user(username))

@app.route('/admin/update_user/<username>', methods=['POST'])
def update_user(username):
    user = get_user_dao().get_user(username)
    if user.password != request.form['password']:
        get_user_dao().edit_password(username, request.form['password'])
    if user.full_name != request.form['full_name']:
        get_user_dao().edit_full_name(username, request.form['full_name'])
    return  redirect('/admin')

@app.route('/admin/users')
def users():
    result = ""
    for user in get_user_DAO().get_users():
        result+= str(user)
    return result
    
#Helper methods
def get_user_dao():
    return PostgresUserDAO()
