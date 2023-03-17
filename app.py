"""Blogly application."""

import os

from flask import Flask, redirect, render_template, request
from models import connect_db, User, db, connect_db, Post
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
    """ redirects to list of users """

    return redirect('/users')


@app.get('/users')
def get_users_page():
    """ shows all users with add user button """

    users = User.query.all()

    return render_template('users.html', users=users)

@app.get('/users/new')
def show_new_user_form():
    """ shows new user sign up form """

    return render_template('new.html')

@app.post('/users/new')
def process_add_form():
    """ process the add form inputs and redirects to users page """

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form.get('image_url') #dont need get because form will always have image_url

    image_url = image_url if image_url else None #either pass in empty string or default image

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user)

    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>')
def show_user_info(user_id):
    """ shows user details """

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id).all()

    return render_template('details.html',user=user, posts=posts)

@app.get('/users/<int:user_id>/edit')
def show_edit_user(user_id):
    """ shows edit page for a specific user """

    user = User.query.get_or_404(user_id)

    return render_template('edit.html', user=user)

@app.post('/users/<int:user_id>/edit')
def edit_user(user_id):
    """ processes user edit form values and redirects to users page """

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    user.image_url = user.image_url if user.image_url else None

    db.session.commit()

    return redirect ("/users")

@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """ deletes the user and redirects to users page """

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')



# PART 2

@app.get('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """ shows user the create new post form """

    user = User.query.get_or_404(user_id)

    return render_template('new_post.html', user=user)

@app.post('/users/<int:user_id>/posts/new')
def process_post_form(user_id):
    """ processes post form values and redirects to user detail page """

    user = User.query.get_or_404(user_id)

    title = request.form['post_title']
    content = request.form['post_content']

    new_post = Post(title=title, content=content, created_at='2023-03-03', user_id=user.id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.get('/posts/<int:post_id>')
def show_post(post_id):
    """ show form to add post """

    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    user = User.query.get(user_id)

    return render_template('post_details.html', post = post, user = user)

@app.get('/posts/<int:post_id>/edit')
def show_edit_post(post_id):
    """ show post edit form """

    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    user = User.query.get(user_id)

    return render_template("post_edit.html", post=post, user=user)

@app.post('/posts/<int:post_id>/edit')
def process_post_edit(post_id):
    """ processes the post edit form inputs """

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")

@app.post('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """ deletes the post from the db """

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')