from flask import request, session
from app import app
from app.utils import calculators


@app.route("/api/bmi", methods=["POST"])
def bmi():
    if "user" not in session:
        return {"message": "user not signed in"}, 401

    data = request.get_json()

    user_height = data.get("height", "")
    user_weight = data.get("weight", "")

    if user_weight == "":
        return {"message": "weight missing"}, 400
    elif user_height == "":
        return {"message": "height missing"}, 400

    bmi = calculators.BMICalculator(float(user_weight), float(user_height))

    return {"message": "success", "BMI": bmi}, 200
