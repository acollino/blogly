"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, Tag, PostTag
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_default")
uri = os.getenv("DATABASE_URL", "postgresql:///blogly")
if uri.startswith("postgres://"):  # since heroku uses 'postgres', not 'postgresql'
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug = True

connect_db(app)


@app.before_first_request
def seed_table():
    db.drop_all()
    db.create_all()
    seed_users = [User(first_name="Jon", last_name="Snow", image_url="https://cdn.pixabay.com/photo/2019/12/05/11/10/snowman-4674856_960_720.jpg"),
                  User(first_name="Kermit", last_name="The Frog",
                       image_url="https://cdn.pixabay.com/photo/2020/06/20/01/24/frog-5319326_960_720.jpg"),
                  User(first_name="Santa", image_url="https://cdn.pixabay.com/photo/2017/11/20/15/38/santa-claus-2965863_960_720.jpg")]
    db.session.add_all(seed_users)
    db.session.commit()


@app.route("/")
def redirect_to_users():
    """Redirects to the list of users."""
    return redirect("/users")


@app.route("/users")
def display_users():
    """Displays the list of all users."""
    db_users = User.query.all()
    return render_template("index.html", users=db_users)


@app.route("/users/new")
def show_add_user_form():
    """Displays the form for adding a new user."""
    return render_template("new_user.html")


@app.route("/users/new", methods=["POST"])
def add_user():
    """Adds a new user to the database, then displays all users."""
    url = None
    if request.form.get("url") != "":
        url = request.form.get("url")
    new_user = User(first_name=request.form.get("first_name"),
                    last_name=request.form.get("last_name"),
                    image_url=url)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<user_id>")
def user_details(user_id):
    """Displays the details of a specific user."""
    user = User.query.get_or_404(user_id) #consider using join to reduce number of SQL calls being made
    return render_template("user_details.html", user=user)


@app.route("/users/<user_id>/edit")
def show_edit_user_form(user_id):
    """Displays the form for editing details about a user."""
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)


@app.route("/users/<user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """Updates the edited user in the database, then displays all users."""
    user = User.query.get_or_404(user_id)
    if request.form.get("first_name") != "":
        user.first_name = request.form.get("first_name")
    if request.form.get("last_name") != "":
        user.last_name = request.form.get("last_name")
    if request.form.get("url") != "":
        user.image_url = request.form.get("url")
    db.session.add(user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Removes a user from the database, then displays all users."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<user_id>/posts/new")
def show_add_post_form(user_id):
    """Shows the form to add a post for this user."""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("new_post.html", user=user, tags=tags)


@app.route("/users/<user_id>/posts/new", methods=["POST"])
def add_user_post(user_id):
    """Adds the submitted post for this user, then displays user details."""
    post_title = None
    if request.form.get("title") != "":
        post_title = request.form.get("title")
    post = Post(title=post_title, content=request.form.get(
        "content"), user_id=user_id)
    db.session.add(post)
    db.session.commit()
    tags = Tag.query.filter(Tag.name.in_(request.form.getlist("tag"))).all()
    post.tags.extend(tags)
    db.session.commit()
    return redirect(f"/users/{user_id}")


@app.route("/posts/<post_id>")
def show_post_details(post_id):
    """Show the details of a post."""
    post = Post.query.get_or_404(post_id)
    return render_template("post_details.html", post=post)


@app.route("/posts/<post_id>/edit")
def show_edit_post_form(post_id):
    """Displays the form for editing details about a post."""
    post = Post.query.get_or_404(post_id)
    return render_template("edit_post.html", post=post)


@app.route("/posts/<post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """Updates the edited post in the database, then displays that post."""
    post = Post.query.get_or_404(post_id)
    if request.form.get("title") != "":
        post.title = request.form.get("title")
    if request.form.get("content") != "":
        post.content = request.form.get("content")
    db.session.add(post)
    db.session.commit()
    return redirect(f"/posts/{post_id}")


@app.route("/posts/<post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Removes a post from the database, then displays the post creator details."""
    post = Post.query.get_or_404(post_id)
    user = post.user
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{user.id}")


@app.route("/tags")
def show_tags():
    """Show all tags, with links to the tag detail pages."""
    tags = Tag.query.all()
    return render_template("tags.html", tags=tags)


@app.route("/tags/<tag_id>")
def show_tag_details(tag_id):
    """Show the details of a tag, listing the related posts."""
    tag = Tag.query.get_or_404(tag_id)
    posts = db.session.query(Post).join(Post.tags).all()
    return render_template("tag_details.html", tag=tag, posts=posts)


@app.route("/tags/new")
def show_add_tag_form():
    """Shows the form to add a tag."""
    return render_template("new_tag.html")


@app.route("/tags/new", methods=["POST"])
def add_tag():
    """Adds the submitted tag to the database, then redirects to the tags list."""
    tag = Tag(name=request.form.get("name"))
    db.session.add(tag)
    db.session.commit()
    return redirect("/tags")


@app.route("/tags/<tag_id>/edit")
def show_edit_tag_form(tag_id):
    """Displays the form for editing the details of a tag."""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("edit_tag.html", tag=tag)


@app.route("/tags/<tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """Updates the edited tag in the database, then redirects to the tags list."""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form.get("name")
    db.session.add(tag)
    db.session.commit()
    return redirect("/tags")


@app.route("/tags/<tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Removes a tag from the database, then redirects to the tags list."""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect("/tags")
