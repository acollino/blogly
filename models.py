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
    image_url = db.Column(
        db.String(), default="/static/assets/default_user_profile.png")

    posts = db.relationship("Post", cascade="delete", backref="user")

    @property
    def fullname(self):
        """Resturns the full name of the User"""
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
    created_at = db.Column(
        db.DateTime, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id", ondelete="CASCADE"))

    tags = db.relationship("Tag", secondary="post_tags", backref="posts")

    @property
    def created_display(self):
        """Returns a more readable time for the post's creation."""
        return self.created_at.strftime("%I:%M %p on %b %d, %Y")


class Tag(db.Model):
    """Class representing a tag on a post in the tags table."""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), unique=True, nullable=False)


class PostTag(db.Model):
    """Class representing the post-tag pairs in the post_tags junction table."""

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey(
        "tags.id", ondelete="CASCADE"), primary_key=True)
