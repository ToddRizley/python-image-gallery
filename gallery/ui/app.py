from flask import Flask, flash, request, render_template, redirect, session
from gallery.data.db import connect
from gallery.data.user import User
from gallery.data.image import Image
from gallery.data.postgres_image_dao import PostgresImageDAO
from gallery.data.postgres_user_dao import PostgresUserDAO
from gallery.aws.secrets import get_secret_flask_session
from functools import wraps
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = get_secret_flask_session()
S3_BUCKET = 'edu.au.cc.image-gallery.tzr'

connect()

def check_admin():
    return session["is_admin"]

def check_auth():
    return 'username' in session

def requires_admin(view):
    @wraps(view)
    def decorated(**kwargs):
        if not check_admin():
            return redirect('/login')
        return view(**kwargs)
    return decorated

def requires_authentication(view):
    @wraps(view)
    def decorated(**kwargs):
        if not check_auth():
            return redirect('/login')
        return view(**kwargs)
    return decorated

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
        session["is_admin"] = user.is_admin
        
        return redirect("/")
    
@app.route('/invalid_login')
def invalid_login():
    ##message flash redirect to /login
    return render_template('invalid_login.html')

@app.route('/')
@requires_authentication
def main_menu():
    return render_template('main.html', username=session["username"], is_admin=session["is_admin"])

@app.route('/upload_image')
@requires_authentication
def upload_image():
    return render_template('upload_image.html')

@app.route('/upload_image_exec', methods=['POST'])
@requires_authentication
def upload_exec():
    uploaded_file = request.files['upload_image']
    if uploaded_file.filename != '':
        file_path = session['username'] + "/" + secure_filename(uploaded_file.filename)
        get_image_dao().add_image(S3_BUCKET,file_path, session['username'], uploaded_file)
        flash('Photo selected and uploaded')
    return redirect('/')


@app.route('/images/<username>')
@requires_authentication
def view_images(username):
    ## get user images
    images = get_image_dao().get_images_for_username(S3_BUCKET, username) 
    ## render user images in template
    return render_template('view_images.html', images=images, username=username)

@app.route('/delete_image/<username>/<image_id>')
@requires_authentication
def delete_image(username, image_id):
    image = get_image_dao().get_image_by_id_and_username(image_id, username)
    get_image_dao().delete_user_image(S3_BUCKET, image)
    flash('Image Deleted!')
    return redirect('/images/'+ username)

@app.route('/admin')
@requires_admin
@requires_authentication
def admin():
    return render_template('admin.html', users= get_user_dao().get_users())

@app.route('/admin/add_new_user')
@requires_admin
@requires_authentication
def add_new_user():
    return render_template("add_new_user.html")

@app.route('/admin/create_user', methods=['POST'])
@requires_admin
@requires_authentication
def create_user():
    get_user_dao().add_user(request.form['username'], request.form['password'], request.form['full_name'], request.form['is_admin'])
    return  redirect('/admin')

@app.route('/admin/deletion_confirmation/<username>', methods=['GET'])
@requires_admin
@requires_authentication
def deletion_confirmation(username):
    return render_template("deletion_confirmation.html", username=username)

@app.route('/admin/delete_user/<username>', methods=['POST'])
@requires_admin
@requires_authentication
def delete_user_route(username):
    get_user_dao().delete_user(username)
    return  redirect('/admin')

@app.route('/admin/edit_user/<username>', methods=['GET'])
@requires_admin
@requires_authentication
def edit_user(username):
    return render_template("edit_user.html", user= get_user_dao().get_user(username))

@app.route('/admin/update_user/<username>', methods=['POST'])
@requires_admin
@requires_authentication
def update_user(username):
    user = get_user_dao().get_user(username)
    if user.password != request.form['password']:
        get_user_dao().edit_password(username, request.form['password'])
    if user.full_name != request.form['full_name']:
        get_user_dao().edit_full_name(username, request.form['full_name'])
    return  redirect('/admin')

@app.route('/admin/users')
@requires_admin
@requires_authentication
def users():
    return redirect('/admin')

#Helper methods

def get_image_dao():
    return PostgresImageDAO()

def get_user_dao():
    return PostgresUserDAO()
