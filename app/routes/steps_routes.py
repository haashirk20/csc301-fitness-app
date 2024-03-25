from flask import request, session
from app import app
from app.models import User
from app.utils import steps_utils
import datetime
import json


@app.route("/api/steps/add", methods=["POST"])
def steps_add():
    if "user" not in session:
        return {"message": "user not signed in"}, 401

    data = request.get_json()
    steps = data.get("steps", "")
    if steps == "":
        return {"message": "steps missing"}, 400
    if int(steps) < 1:
        return {"message": "steps must be greater than 0"}, 400

    user = User.User(id=session["user"]["id"])
    updated_steps = user.steps_add(int(steps))

    return {"message": "success", "steps": updated_steps}, 200


@app.route("/api/steps/today")
def steps_today():
    if "user" not in session:
        return {"message": "user not signed in"}, 401

    user = User.User(id=session["user"]["id"])
    all_steps = user.get_steps()

    today_date = datetime.date.today().isoformat()
    if today_date not in all_steps:
        steps = user.steps_reset([today_date])
    else:
        steps = all_steps.get(today_date)

    # As requested by frontend
    if steps == 0:
        steps = None

    return {"message": "success", "steps": steps}, 200


@app.route("/api/steps/week")
def steps_week():
    if "user" not in session:
        return {"message": "user not signed in"}, 401

    user = User.User(id=session["user"]["id"])

    # Number of days passed since last Sunday
    dayCode = datetime.date.today().weekday()
    days_passed = (dayCode - 6) % 7 + 1
    result = steps_utils.get_last_steps(user, days_passed)

    return {
        "message": "success",
        "steps": json.dumps(result["steps"]),
        "totalSteps": result["total_steps"],
    }, 200


@app.route("/api/steps/month")
def steps_month():
    if "user" not in session:
        return {"message": "user not signed in"}, 401

    user = User.User(id=session["user"]["id"])
    days_passed = datetime.date.today().day
    result = steps_utils.get_last_steps(user, days_passed)

    return {
        "message": "success",
        "steps": json.dumps(result["steps"]),
        "totalSteps": result["total_steps"],
    }, 200