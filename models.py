from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)

"""Models for Blogly."""
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True)
    
    first_name = db.Column(
        db.String(20),
        nullable = False)

    last_name = db.Column(
        db.String(20),
        nullable = False)
    
    image_url = db.Column(
        db.String(100))

