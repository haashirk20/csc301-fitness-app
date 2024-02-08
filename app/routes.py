from app import app
from flask import request, session, redirect, url_for
import re
from app import models


@app.route("/api/login", methods=["POST"])
def login():
    if "user" in session:
        return {"message": "user already signed in"}

    user_name = request.args.get("name", "")
    user_pass = request.args.get("password", "")

    if user_name == "":
        return {"message": "name missing"}, 400
    elif user_pass == "":
        return {"message": "password missing"}, 400

    user = models.User(name=user_name, password=user_pass)

    if user.login():
        session["user"] = user.__dict__  # save user model or user id?
        return {"message": "user signed in"}, 200
    else:
        # we don't have to specify which one of email or password failed,
        # since that could be a security risk (reveals if email exists)
        return {"message": "incorrect email or password"}, 401


# basic signup route
@app.route("/api/signup", methods=["POST"])
def signup():
    if "user_id" in session:
        return {"message": "user already signed in"}

    user_email = request.args.get("email", "").lower()
    user_name = request.args.get("name", "")
    user_age = request.args.get("age", "")
    user_pass = request.args.get("password", "")

    if user_name == "":
        return {"message": "name missing"}, 400
    elif user_age == "":
        return {"message": "age missing"}, 400
    if user_email == "":
        return {"message": "email missing"}, 400
    elif user_pass == "":
        return {"message": "password missing"}, 400

    # check if email is valid
    if not re.match(r"[^@]+@[^@]+\.[^@]+", user_email):
        return {"message": "invalid email"}, 400

    user = models.User(
        name=user_name, password=user_pass, email=user_email, age=user_age
    )

    if user.signup():
        return {"message": "user created"}, 200
    else:
        return {"message": "user already exists"}, 400
