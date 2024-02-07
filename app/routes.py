from app import app
from flask import request, session, redirect, url_for
import re
from app import models


@app.route("/")
def home():
    if "user_id" in session:
        return f"Hey, {session['user_id']}! You are authenticated."
    else:
        return "Hey, anonymous user! You are not authenticated."


@app.route("/api/login", methods=["POST"])
def login():
    if "user_id" in session:
        return {"message": "user already signed in"}

    user_email = request.args.get("email", "").lower()
    user_pass = request.args.get("password", "")

    if user_email == "":
        return {"message": "email missing"}, 400
    elif user_pass == "":
        return {"message": "password missing"}, 400

    user = models.User.login(user_email, user_pass)

    if user:
        session["user_id"] = user
        return redirect(url_for("home"))
    else:
        # we don't have to specify which one of email or password failed,
        # since that could be a security risk (reveals if email exists)
        return {"message": "incorrect email or password"}, 401
    
#basic signup route
@app.route("/api/signup", methods=["POST"])
def signup():
    if "user_id" in session:
        return {"message": "user already signed in"}

    user_email = request.args.get("email", "").lower()
    user_pass = request.args.get("password", "")

    #TODO implement birthday storing
    #user_bday = request.args.get("birthday", "")

    if user_email == "":
        return {"message": "email missing"}, 400
    elif user_pass == "":
        return {"message": "password missing"}, 400

    #check if email is valid
    if not re.match(r"[^@]+@[^@]+\.[^@]+", user_email):
        return {"message": "invalid email"}, 400

    user = models.User(user_email, user_pass)
    user.save_to_db()

    return redirect(url_for("home"))
