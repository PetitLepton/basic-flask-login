import os
from flask import Flask, render_template, redirect, request, session
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, PasswordField, SubmitField

application = Flask(__name__, instance_relative_config=True)
application.config.from_pyfile("config.py")
csrf = CSRFProtect(application)

application.config["DEBUG"] = True


@application.before_request
def is_logged_in():
    if not session.get("logged_in") and request.endpoint not in ("login", "static"):
        session["url"] = request.url
        return redirect("/login")


class UserForm(FlaskForm):
    username = StringField(label="Username")
    password = PasswordField(label="Password")
    submit = SubmitField(label="Log in")


@application.route("/login", methods=["GET", "POST"])
def login():
    form = UserForm()
    status = 200
    if form.validate_on_submit():
        args = dict(**form.data)
        username = args.get("username")
        password = args.get("password")
        if (
            username == application.config["BASIC_AUTH_USERNAME"]
            and password == application.config["BASIC_AUTH_PASSWORD"]
        ):
            session["logged_in"] = True
            return redirect(session.get("url", "/"))
        else:
            form.errors["wrong_password"] = ["Wrong username and/or password"]
            status = 401
    return render_template("login.html", form=form), status


@application.route("/")
def index():
    return "Index"


@application.route("/page-1")
def page_1():
    return "page-1"


if __name__ == "__main__":
    application.secret_key = os.urandom(12)
    application.run(port="5000")
