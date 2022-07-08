"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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
    image_url = db.Column(db.String(), default="/static/assets/default_user_profile.png")

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"
