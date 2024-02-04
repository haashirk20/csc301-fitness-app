def calculate_calorie(age, sex, height, weight, activity="sedentary", goal="maintain"):
    # height stored in cm.
    # weight stored in kg.
    # activity which represents activity level of user can take values "sedentary", "lightly_active",
    # "moderately_active", "very_active", "extra_active".
    # goal which represents whether the user wants to gain, lose or maintain weight can take values "gain", "lose",
    # "maintain".
    # Sources : https://www.bodybuilding.com/fun/macronutcal.htm,
    # https://www.calculator.net/calorie-calculator.html (Mifflin-St Jeor Equation) - This has more detailed weight
    # gain and loss calorie specifications; This function can be changed to mimic the detailed calculator if required.
    if sex == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif sex == "female":
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        # not sure what to do for this case.1500 is minimum calorie recommendation.
        # Can use default as male or female instead maybe. Or maybe return Cannot calculate calories.
        return 1500
    if activity == "sedentary":
        calorie_count = bmr * 1.2
    elif activity == "lightly_active":
        calorie_count = bmr * 1.375
    elif activity == "moderately_active":
        calorie_count = bmr * 1.550
    elif activity == "very_active":
        calorie_count = bmr * 1.725
    elif activity == "extra_active":
        calorie_count = bmr * 1.9
    else:
        return "unidentified activity level"
    if goal == "maintain":
        return calorie_count
    elif goal == "gain":
        return calorie_count + 500
    elif goal == "lose":
        return (80/100) * calorie_count
    else:
        return "unidentified goal"
