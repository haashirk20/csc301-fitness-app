from app import app
from flask import request, session, redirect, url_for
import re
from app import models, calorie

@app.route("/api/login", methods=["POST"])
def login():
    if "user" in session:
        return {"message": "user already signed in"}, 200

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
    if "user" in session:
        return {"message": "user already signed in"}, 400

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
    

@app.route("/api/calories", methods=["GET", "POST"])
def calories():
    if "user" not in session:
      return {"message": "user not signed in"}, 401

    user = models.User(id=session["user"]["id"], name=session["user"]["name"])
    
    if request.method == "GET":
        user_calories_needed = user.get_calories_needed()
        user_calories_remaining = user.get_calories_remaining()
        return {"message": "success", "caloriesNeeded": user_calories_needed, "caloriesRemaining": user_calories_remaining}, 200
    
    elif request.method == "POST":

        # check that form fields are valid
        user_age = request.args.get("age", "")
        user_sex = request.args.get("sex", "")
        user_height = request.args.get("height", "")
        user_weight = request.args.get("weight", "")
        user_activity = request.args.get("activity", "")
        user_goal = request.args.get("goal", "")

        # assume height/weight are numbers and not letters
        if user_age == "":
            return {"message": "age invalid"}, 400
        elif user_sex not in ["male", "female"]:
            return {"message": "sex invalid"}, 400
        elif user_height == "":
            return {"message": "height missing"}, 400
        elif user_weight == "":
            return {"message": "weight missing"}, 400
        elif user_activity not in ["sedentary", "lightly_active", "moderately_active", "very_active", "extra_active"]:
            return {"message": "activity invalid"}, 400
        elif user_goal not in ["maintain", "lose", "gain"]:
            return {"message": "goal invalid"}, 400

        # calculate and return daily needed calories
        calories = calorie.calculate_calorie(int(user_age), user_sex, float(user_height), float(user_weight), user_activity, user_goal)

        user.set_calories(calories)
        return {"message": "success", "caloriesNeeded": calories}, 200


@app.route("/api/calories/reduce", methods=["POST"])
def calories_reduce():
    if "user" not in session:
        return {"message": "user not signed in"}, 401

    user = models.User(id=session["user"]["id"], name=session["user"]["name"])    
    
    calories_used = request.args.get("calories", "")
    if calories_used == "":
        return {"message": "calories invalid"}, 400
    user.calories_reduce(int(calories_used))

    return {"caloriesRemaining": user.get_calories_remaining()}, 200


@app.route("/api/calories/reset", methods=["POST"])
def calories_reset():
    if "user" not in session:
        return {"message": "user not signed in"}, 401

    user = models.User(id=session["user"]["id"], name=session["user"]["name"])        
    user.calories_reset() # sets user.calories_needed and user.calories_remaining

    return {"message": "success", "caloriesNeeded": user.get_calories_needed(), "caloriesRemaining": user.get_calories_remaining()}, 200
