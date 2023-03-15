"""Blogly application."""

import os

from flask import Flask, redirect, render_template, request
from models import connect_db, User, db, connect_db
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'its a secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.get('/')
def get_root_directory():
    """ """

    return redirect('/users');


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
