from flask import request, session
import requests
from app import app
from app.models import User
from app.utils import calorie
import json


@app.route("/api/search", methods=["POST"])
def search():
    # if "user" not in session:
    #     return {'message': 'user not signed in'}, 401

    data = request.get_json()
    query = data.get("query", "").lower()

    user = User.User()
    user_list = user.get_all_users()
    search_results = []
    user_search_results = []
    calories = []
    age = []
    email = []
    sleep = []
    # find similar usernames as query and info to saerch results
    for user in user_list:
        if query in user["name"].lower():
            user_search_results.append(user["name"])
            age.append(user["age"])
            email.append(user["email"])
            # if user has not initalized calories or sleep goals
            try:
                calories.append(user["calories_needed"])
            except:
                calories.append(0)

            try:
                sleep.append(user["sleep"]["goal"])
            except:
                sleep.append(0)

    if len(user_search_results) == 0:
        return {"message": "no results found"}, 404
    search_results.append(user_search_results)
    search_results.append(age)
    search_results.append(email)
    search_results.append(calories)
    search_results.append(sleep)

    return {"message": "success", "results": search_results}, 200
