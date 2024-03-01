from flask import request, session
import requests
from app import app
from app.models import User
from app.utils import calorie
import json


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
        return {"message": "success", "caloriesNeeded": calories}, 200


## Calorie limit set
@app.route("/api/calories/limit", methods=["POST"])
def calories_set():
    if "user" not in session:
        return {"message": "user not signed in"}, 401

    user = User.User(id=session["user"]["id"], name=session["user"]["name"])


    data = request.get_json()
    calories_needed = data.get("calories", "")
    if calories_needed == "":
        return {"message": "calories invalid"}, 400
    user.set_calories(int(calories_needed))

    return {"caloriesNeeded": user.get_calories_needed()}, 200


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

# Created as replacement for calories_reduce, takes food name
@app.route("/api/calories/food", methods=["POST"])
def food():
    if "user" not in session:
        return {"message": "user not signed in"}, 401

    data = request.get_json()

    query = data.get("food_name", "")
    with open("app/utils/api.json") as f:
        api_key = json.load(f).get("APIKEY")
        if api_key is None:
            return {"message": "api key not found"}, 500
    api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
    response = requests.get(api_url, headers={'X-Api-Key': api_key})
    if response.status_code != requests.codes.ok:
        return {"message": "food not found"}, response.status_code
    
    # need to parse the response to get the calories
    # this is placeholder until response format is known
    calories_used = response.json()[0].get("calories")

    # reduce cals if needed
    #user.calories_reduce(int(calories_used))

    return {"calories": int(calories_used)}, 200

@app.route("/api/calories/reset", methods=["GET"])
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
