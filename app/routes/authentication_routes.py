from flask import request, session
import re
from app import app
from app.models import User


@app.route("/api/login", methods=["POST"])
def login():
    if "user" in session:
        return {"message": "user already signed in"}, 200

    data = request.get_json()

    user_name = data.get("name", "")
    user_pass = data.get("password", "")

    if user_name == "":
        return {"message": "name missing"}, 400
    elif user_pass == "":
        return {"message": "password missing"}, 400

    user = User.User(name=user_name, password=user_pass)

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

    data = request.get_json()

    user_email = data.get("email").lower()
    user_name = data.get("name", "")
    user_age = data.get("age", "")
    user_pass = data.get("password", "")

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

    user = User.User(name=user_name, password=user_pass, email=user_email, age=user_age)

    if user.signup():
        return {"message": "user created"}, 200
    else:
        return {"message": "user already exists"}, 400
