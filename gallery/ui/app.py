from flask import Flask
from flask import request
from flask import render_template
from flask import redirect, url_for
#from python-image-gallery.gallery.tools import db
from gallery.tools.db import *
app = Flask(__name__)
#global db_instance 
#db_instance = DBConnector()
#db_instance.connect()


@app.route("/admin/deletion_confirmation/<username>", methods=["POST"])
def deletion_confirmation(username):
    return render_template("deletion_confirmation.html", username=username)

@app.route('/admin/add_user', methods=['POST', 'GET'])
def add_user():
    if request.method == 'GET':
        return render_template("add_user.html")
    elif request.method == 'POST':
        username = request.form['username']
        full_name = request.form['full_name']
        password = request.form['password']
        ##add db
        return redirect('/admin/list_users')

@app.route('/admin/edit_user/<username>', methods=['GET', 'POST'])
def edit_user(username):

    if request.method == 'GET':
        user = {'username':'barney', 'password':'buzz', 'full_name':'Barney Rubble'}
        return render_template("edit_user.html", user=user)
    elif request.method == 'POST':
        username = request.form['username']
        full_name = request.form['full_name']
        password = request.form['password']
        return redirect('/admin/list_users')

@app.route('/admin/delete_user/<username>', methods=['POST'])
def delete_user(username):
    return redirect("/admin/list_users")

@app.route("/admin/list_users", methods=['GET'])
def list_users():
#    db_instance = DBConnector()
#    db_instance.connect()
#    users = db_instance.get_users()
    users = [{'username':'barney', 'password':'buzz', 'full_name':'Barney Rubble'}, {'username':'betty', 'password':'fizz', 'full_name':'Betty Rubble'}]
            
    return render_template("index.html", users=users)
