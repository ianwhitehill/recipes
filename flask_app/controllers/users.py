from types import resolve_bases
from flask.helpers import flash
from flask_app import app
from flask import render_template, redirect, session, request

from flask_app.models.user import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def redirect_to_index():
    return redirect('/user')

@app.route('/user')
def index():
    return render_template('index.html')

@app.route('/user/create', methods=['POST'])
def create_user():
    if User.validate_user(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            "first_name" : request.form['first_name'],
            "last_name" : request.form['last_name'],
            "email" : request.form['email'],
            "password" : pw_hash
        }
        User.insert(data)
        flash("User created please login")
        return redirect('/user')
    else:
        flash("Registration Failed")
        return redirect('/user')

@app.route('/user/login', methods=['POST'])
def user_login():
    users = User.get_by_email(request.form)

    if len(users) == 1:
        user = users[0]
        if bcrypt.check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            session['name'] = f"{user.first_name} {user.last_name}"
            return redirect('/success')
        else:
            flash("Login Failed")
            return redirect('/user')
    else:
        flash("Login Failed")
        return redirect('/user')
    

@app.route('/success')
def success():
    if not 'user_id' in session:
        flash('unable to Login, try again')
        return redirect('/user')
    else:
        return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    flash('you have been logged out')
    return redirect('/user')