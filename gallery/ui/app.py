from flask import Flask, request, render_template, url_for, redirect
from gallery.tools.db import *

app = Flask(__name__)

@app.route('/admin')
def admin():
    db_instance = DBConnector()
    db_instance.connect()
    res  = db_instance.get_users()
    return render_template('admin.html', users=prepare_user_list(res))

@app.route('/admin/add_user')
def add_user():
    return render_template("add_user.html")

@app.route('/create_user', methods=['POST'])
def create_user():
    db_instance = DBConnector()
    db_instance.connect()

    username = request.form['username']
    full_name = request.form['full_name']
    password = request.form['password']
    db_instance.add_user(username, password, full_name)

    res  = db_instance.get_users()
    return render_template('admin.html', users=prepare_user_list(res))

@app.route('/admin/deletion_confirmation/<username>', methods=['GET'])
def deletion_confirmation(username):
    return render_template("deletion_confirmation.html", username=username)

@app.route('/delete_user/<username>', methods=['POST'])
def delete_user(username):
    db_instance = DBConnector()
    db_instance.connect()
    db_instance.delete_user(username)

    res  = db_instance.get_users()
    return render_template('admin.html', users=prepare_user_list(res))

@app.route('/admin/edit_user/<username>', methods=['GET'])
def edit_user(username):
    db_instance = DBConnector()
    db_instance.connect()
    
    row = db_instance.get_user(username).fetchone()
    user = {'username': row[0], 'password': row[1], 'full_name': row[2]}
    return render_template("edit_user.html", user=user)

@app.route('/update_user/<username>', methods=['POST'])
def update_user(username):
    full_name = request.form['full_name']
    password = request.form['password']
    
    db_instance = DBConnector()
    db_instance.connect()

    row = db_instance.get_user(username).fetchone()
    user = {'username': row[0], 'password': row[1], 'full_name': row[2]}

    if user['password'] != password:
        db_instance.edit_password(username, password)
    if user['full_name'] != full_name:
        db_instance.edit_full_name(username, full_name)

    res  = db_instance.get_users()
    return render_template('admin.html', users=prepare_user_list(res))

#Helper methods
def prepare_user_list(users_object):
    result = []
    for row in users_object:
        result.append({'username': row[0], 'full_name':row[1]})
    return result
