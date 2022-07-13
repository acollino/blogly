"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_default")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL', "postgresql:///blogly")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug = True

connect_db(app)
db.drop_all()
db.create_all()


@app.before_first_request
def seed_table():
    User.query.delete()
    Post.query.delete()
    seed_users = [User(first_name="Jon", last_name="Snow", image_url="https://upload.wikimedia.org/wikipedia/commons/2/22/Snowman_in_Indiana_2014.jpg"),
                  User(first_name="Kermit", last_name="The Frog",
                       image_url="https://upload.wikimedia.org/wikipedia/en/6/62/Kermit_the_Frog.jpg"),
                  User(first_name="Pikachu", image_url="https://assets.pokemon.com/assets/cms2/img/pokedex/full/025.png")]
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
    user = User.query.get_or_404(user_id)
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
def show_post_form(user_id):
    """Shows the form to add a post for this user."""
    user = User.query.get_or_404(user_id)
    return render_template("new_post.html", user=user)


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
