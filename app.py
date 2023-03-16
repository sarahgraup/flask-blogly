"""Blogly application."""

import os

from flask import Flask, redirect, render_template, request
from models import connect_db, User, db, connect_db
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import update


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'its a secret'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.get('/')
def get_root_directory():
    """ """

    return redirect('/users')


@app.get('/users')
def get_users_page():
    """  """

    users = User.query.all()

    return render_template('users.html', users=users)

@app.get('/users/new')
def show_new_user_form():
    """  """

    return render_template('new.html')

@app.post('/users/new')
def process_add_form():
    """  """

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form.get('image_url')

    image_url = image_url if image_url else None

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user)

    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>')
def show_user_info(user_id):
    """ """
    user = User.query.get(user_id)
    return render_template('details.html',user = user)
@app.get('/users/<int:user_id>/edit')
def show_edit_user(user_id):
    user = User.query.get(user_id)
    return render_template('edit.html', user=user)

@app.post('/users/<int:user_id>/edit')
def edit_user(user_id):
    user = User.query.get(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form.get('image_url')

    db.session.commit()
    return redirect ("/users")





# stmt = (
# ...     update(user_table)
# ...     .where(user_table.c.name == "patrick")
# ...     .values(fullname="Patrick the Star")
# ... )