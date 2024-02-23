from flask import request, session
from app import app
from app.models import User
from app.utils import calorie


@app.route("/api/calories", methods=["GET", "POST"])
def calories():
    if "user" not in session:
        return {"message": "user not signed in"}, 401

    user = User.User(id=session["user"]["id"], name=session["user"]["name"])

    if request.method == "GET":
        user_calories_needed = user.get_calories_needed()
        user_calories_remaining = user.get_calories_remaining()
        return {
            "message": "success",
            "caloriesNeeded": user_calories_needed,
            "caloriesRemaining": user_calories_remaining,
        }, 200

    elif request.method == "POST":

        data = request.get_json()

        # check that form fields are valid
        user_age = data.get("age", "")
        user_sex = data.get("sex", "")
        user_height = data.get("height", "")
        user_weight = data.get("weight", "")
        user_activity = data.get("activity", "")
        user_goal = data.get("goal", "")

        # assume height/weight are numbers and not letters
        if user_age == "":
            return {"message": "age invalid"}, 400
        elif user_sex not in ["male", "female"]:
            return {"message": "sex invalid"}, 400
        elif user_height == "":
            return {"message": "height missing"}, 400
        elif user_weight == "":
            return {"message": "weight missing"}, 400
        elif user_activity not in [
            "sedentary",
            "lightly_active",
            "moderately_active",
            "very_active",
            "extra_active",
        ]:
            return {"message": "activity invalid"}, 400
        elif user_goal not in ["maintain", "lose", "gain"]:
            return {"message": "goal invalid"}, 400

        # calculate and return daily needed calories
        calories = calorie.calculate_calorie(
            int(user_age),
            user_sex,
            float(user_height),
            float(user_weight),
            user_activity,
            user_goal,
        )

        user.set_calories(calories)
        return {"message": "success", "caloriesNeeded": calories}, 200


@app.route("/api/calories/reduce", methods=["POST"])
def calories_reduce():
    if "user" not in session:
        return {"message": "user not signed in"}, 401

    user = User.User(id=session["user"]["id"], name=session["user"]["name"])

    data = request.get_json()
    calories_used = data.get("calories", "")
    if calories_used == "":
        return {"message": "calories invalid"}, 400
    user.calories_reduce(int(calories_used))

    return {"caloriesRemaining": user.get_calories_remaining()}, 200


@app.route("/api/calories/reset", methods=["POST"])
def calories_reset():
    if "user" not in session:
        return {"message": "user not signed in"}, 401

    user = User.User(id=session["user"]["id"], name=session["user"]["name"])
    user.calories_reset()  # sets user.calories_needed and user.calories_remaining

    return {
        "message": "success",
        "caloriesNeeded": user.get_calories_needed(),
        "caloriesRemaining": user.get_calories_remaining(),
    }, 200
