from flask import request, session
from app import app
from app.models import User
from app.utils import workout_utils
import datetime
import json


@app.route("/api/workout", methods=["POST"])
def workout():
    if "user" not in session:
        return {"message": "user not signed in"}, 401

    # Check that request data is valid
    data = request.get_json()

    if "time" not in data or "sex" not in data or "bodyWeight" not in data:
        return {"message": "time, sex, or bodyWeight missing"}, 400
    if data["sex"] != "male" and data["sex"] != "female":
        return {"message": "sex must be male or female"}, 400
    if "name" not in data or data["name"] == "":
        return {"message": "name missing"}, 400
    if "sets" not in data or data["sets"] == "":
        return {"message": "sets missing"}, 400
    if "reps" not in data or data["reps"] == "":
        return {"message": "reps missing"}, 400
    if "weight" not in data or data["weight"] == "":
        return {"message": "weight missing"}, 400

    try:
        data["time"] = int(data["time"])
        data["bodyWeight"] = int(data["bodyWeight"])
    except:
        return {"message": "time and bodyWeight must be integers"}, 400
    try:
        data["sets"] = int(data["sets"])
        data["reps"] = int(data["reps"])
        data["weight"] = int(data["weight"])
    except:
        return {"message": "sets, reps, and weight must be integers"}, 400

    user = User.User(id=session["user"]["id"])
    today_date = datetime.date.today().isoformat()
    tonnage = workout_utils.tonnage(data["sets"], data["reps"], data["weight"])
    cals_burned = workout_utils.calories_burned(
        data["time"], data["bodyWeight"], data["sex"]
    )
    result = user.set_workout_record(today_date, tonnage, cals_burned)

    return {
        "message": "success",
        "tonsLifted": tonnage,
        "caloriesBurned": cals_burned,
    }, 200


@app.route("/api/workout/today/")
def workout_today():
    if "user" not in session:
        return {"message": "user not signed in"}, 401

    user = User.User(id=session["user"]["id"])
    workout_records = user.get_workout_records()

    today_date = datetime.date.today().isoformat()
    if today_date not in workout_records:
        return {"message": "no workout recorded"}, 404
    else:
        result = workout_records.get(today_date)

    return {
        "message": "success",
        "tonsLifted": result["tonnage"],
        "caloriesBurned": result["calories"],
    }, 200


@app.route("/api/workout/week/")
def workout_week():
    if "user" not in session:
        return {"message": "user not signed in"}, 401

    user = User.User(id=session["user"]["id"])

    # Number of days passed since last Sunday
    dayCode = datetime.date.today().weekday()
    days_passed = (dayCode - 6) % 7 + 1
    print("days_passed", days_passed)
    result = workout_utils.previous_workouts(user, days_passed)

    # As requested by frontend, complete week even if null
    for i in range(1, 7 - days_passed + 1):
        result["workouts"].append(
            {
                "date": (
                    datetime.date.today() + datetime.timedelta(days=i)
                ).isoformat(),
                "day": (datetime.date.today() + datetime.timedelta(days=i)).strftime(
                    "%A"
                ),
                "tonsLifted": None,
                "caloriesBurned": None,
            }
        )

    return {
        "message": "success",
        "workouts": json.dumps(result["workouts"]),
        "tonsLiftedAvg": result["tons_lifted_avg"],
        "caloriesBurnedAvg": result["calories_burned_avg"],
        "tonsLiftedTotal": result["tons_lifted_total"],
        "caloriesBurnedTotal": result["calories_burned_total"],
    }, 200


@app.route("/api/workout/month/")
def workout_month():
    if "user" not in session:
        return {"message": "user not signed in"}, 401

    user = User.User(id=session["user"]["id"])

    # Number of days passed since last Sunday
    days_passed = datetime.date.today().day
    result = workout_utils.previous_workouts(user, days_passed)

    return {
        "message": "success",
        "workouts": json.dumps(result["workouts"]),
        "tonsLiftedAvg": result["tons_lifted_avg"],
        "caloriesBurnedAvg": result["calories_burned_avg"],
        "tonsLiftedTotal": result["tons_lifted_total"],
        "caloriesBurnedTotal": result["calories_burned_total"],
    }, 200


@app.route("/api/workout/days/<int:days>")
def workout_days(days):
    if "user" not in session:
        return {"message": "user not signed in"}, 401

    user = User.User(id=session["user"]["id"])

    # Number of days passed since last Sunday
    result = sleep_utils.previous_sleeps(user, days)

    return {
        "message": "success",
        "sleep": json.dumps(result["sleep"]),
        "hoursAvg": result["hours_avg"],
        "hoursTotal": result["hours_total"],
    }, 200
