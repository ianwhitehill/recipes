from types import resolve_bases
from flask.helpers import flash
from flask_app import app
from flask import render_template, redirect, session, request

from flask_app.models.user import User
from flask_app.models.recipe import Recipe

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/dashboard')
def recipes_dashboard():
    if not 'user_id' in session:
        flash('You must be logined in to view recipes') 
        return redirect('/user')
        
    recipes = Recipe.select_all()
    return render_template('dashboard.html', recipes = recipes, user_name = session['name'])