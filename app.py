"""Blogly application."""

from crypt import methods
from flask import Flask, request, redirect, render_template
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_default")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug = True

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.before_first_request
def seed_table():
    User.query.delete()
    seed_users = [User(first_name="Jon", last_name="Snow", image_url="https://upload.wikimedia.org/wikipedia/commons/2/22/Snowman_in_Indiana_2014.jpg"),
                  User(first_name="Kermit", last_name="The Frog", image_url="https://upload.wikimedia.org/wikipedia/en/6/62/Kermit_the_Frog.jpg"),
                  User(first_name="Pikachu", image_url="https://assets.pokemon.com/assets/cms2/img/pokedex/full/025.png")]
    db.session.add_all(seed_users)
    db.session.commit()


@app.route("/")
def redirect_to_users():
    return redirect("/users")


@app.route("/users")
def display_users():
    db_users = User.query.all()
    return render_template("index.html", users=db_users)


@app.route("/users/new")
def show_add_user_form():
    return render_template("new_user.html")


@app.route("/users/new", methods=["POST"])
def add_user():
    url = None
    if request.form.get("url") != "":
        url = request.form.get("url")
    new_user = User(first_name = request.form.get("first_name"),
                    last_name = request.form.get("last_name"),
                    image_url = url)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<user_id>")
def user_details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user_details.html", user=user)


@app.route("/users/<user_id>/edit")
def show_edit_user_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)

@app.route("/users/<user_id>/edit", methods=["POST"])
def edit_user(user_id):
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
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")