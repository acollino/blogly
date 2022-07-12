"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import time

from sqlalchemy import ForeignKey

db = SQLAlchemy()


def connect_db(app):
    """Connect to the Users database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """Class representing a Blogly user in the users table."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), default="")
    image_url = db.Column(
        db.String(), default="/static/assets/default_user_profile.png")

    @property
    def fullname(self):
        if self.last_name == "":
            return self.first_name
        else:
            return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """Class representing a user's post in the posts table."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(), default="Post Title")
    content = db.Column(db.String(), default="")
    created_at = db.Column(db.DateTime, default=time.strftime("%I:%M %p on %b %d, %Y"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.relationship("User", backref="posts")
