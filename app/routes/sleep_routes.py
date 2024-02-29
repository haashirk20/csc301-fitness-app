from flask import request, session
from app import app
from app.models import User
from app.utils import sleep_utils
import datetime
import json


@app.route("/api/sleep/goal/", methods=["GET", "POST"])
def sleep_goal():
    if "user" not in session:
        return {"message": "user not signed in"}, 401

    if request.method == "GET":
        user = User.User(id=session["user"]["id"])
        goal = user.get_sleep_goal()
        return {"message": "success", "goal": goal}, 200
    elif request.method == "POST":
        data = request.get_json()
        goal = data.get("goal", "")
        if goal == "":
            return {"message": "goal missing"}, 400

        user = User.User(id=session["user"]["id"])
        user.set_sleep_goal(int(goal))
        return {"message": "success"}, 200


@app.route("/api/sleep/", methods=["POST"])
def sleep_add():
    if "user" not in session:
        return {"message": "user not signed in"}, 401

    # Check that request data is valid
    data = request.get_json()
    slept_at_str = data.get("sleptAt", "")
    awake_at_str = data.get("awakeAt", "")
    if slept_at_str == "":
        return {"message": "sleptAt missing"}, 400
    if awake_at_str == "":
        return {"message": "awakeAt missing"}, 400
    try:
        slept_at = datetime.datetime.strptime(slept_at_str, "%Y-%m-%dT%H:%M")
        awake_at = datetime.datetime.strptime(awake_at_str, "%Y-%m-%dT%H:%M")
        if slept_at >= awake_at:
            return {"message": "sleptAt >= awakeAt"}, 400
    except ValueError:
        return {"message": "sleepAt or awakeAt invalid"}, 400

    # If the user went to bed after midnight, their night should belong to the previous day
    if slept_at.date() == awake_at.date():
        date_slept = slept_at.date() - datetime.timedelta(days=1)
    else:
        date_slept = slept_at.date()

    # Get hours slept
    sleep_duration = (awake_at - slept_at).total_seconds()
    hours = int(sleep_duration // 3600)
    minutes = int((sleep_duration % 3600) // 60)
    hours_decimal = round(hours + (minutes / 60), 2)

    user = User.User(id=session["user"]["id"])
    result = user.set_sleep_record(date_slept, hours_decimal)

    return {
        "message": "success",
        "hours": result,
    }, 200


@app.route("/api/sleep/lastnight/")
def sleep_today():
    if "user" not in session:
        return {"message": "user not signed in"}, 401

    user = User.User(id=session["user"]["id"])
    sleep_records = user.get_sleep_records()

    yesterday_date = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    if yesterday_date not in sleep_records:
        result = user.set_sleep_record(yesterday_date, 0.0)
    else:
        result = sleep_records.get(yesterday_date)

    hours = None if result["hours"] == 0.0 else result["hours"]

    return {
        "message": "success",
        "hours": hours,
    }, 200


@app.route("/api/sleep/week/")
def sleep_week():
    if "user" not in session:
        return {"message": "user not signed in"}, 401

    user = User.User(id=session["user"]["id"])

    # Number of days passed since last Sunday
    dayCode = datetime.date.today().weekday()
    days_passed = (dayCode - 6) % 7
    result = sleep_utils.previous_sleeps(user, days_passed)

    return {
        "message": "success",
        "sleep": json.dumps(result["sleep"]),
        "hoursAvg": result["hours_avg"],
        "hoursTotal": result["hours_total"],
    }, 200


@app.route("/api/sleep/month/")
def sleep_month():
    if "user" not in session:
        return {"message": "user not signed in"}, 401

    user = User.User(id=session["user"]["id"])

    # Number of days passed since last Sunday
    dayCode = datetime.date.today().weekday()
    days_passed = datetime.date.today().day
    result = sleep_utils.previous_sleeps(user, days_passed - 1)

    return {
        "message": "success",
        "sleep": json.dumps(result["sleep"]),
        "hoursAvg": result["hours_avg"],
        "hoursTotal": result["hours_total"],
    }, 200
