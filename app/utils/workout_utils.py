import datetime


def tonnage(workouts):
    total_tons = 0
    # weight_metric = 907.185 # if weight is kg
    weight_metric = 2000  # if weight is lbs
    for exercise in workouts:
        total_tons += (
            int(exercise["sets"])
            * int(exercise["reps"])
            * int(exercise["weight"])
            / weight_metric
        )
    return total_tons


def calories_burned(time, weight, sex):
    # source: https://www.strengthlog.com/calories-burned-lifting-weights/#:~:text=Calories%20Burned%20Lifting%20Weights
    cals_burned = 0
    if sex == "male":
        cals_burned = time * weight * 0.0713
    if sex == "female":
        cals_burned = time * weight * 0.0637
    print("cals_burned", cals_burned)
    return cals_burned


def previous_workouts(user, days):
    workout_records = user.get_workout_records()
    print("days", days, "records", workout_records)
    workouts_arr = []
    today_date = datetime.date.today()
    total_tons = 0
    total_cals_burned = 0.0
    days_accounted_for = 0

    # It's counting down not up, so that today's date is last item in array for chronological order
    for i in range(days - 1, -1, -1):
        date = today_date - datetime.timedelta(days=i)
        date_str = date.isoformat()
        print("DAY", i, date_str)

        # if user didn't record workout for that day:
        if date_str not in workout_records:
            tons = None
            cals_burned = None
        else:
            tons = workout_records.get(date_str).get("tonnage")
            cals_burned = workout_records.get(date_str).get("calories")
            total_tons += tons
            total_cals_burned += cals_burned
            days_accounted_for += 1

        workouts_arr.append(
            {
                "date": date_str,
                "day": date.strftime("%A"),
                "tonsLifted": tons,
                "caloriesBurned": cals_burned,
            }
        )
        print("workouts_arr", workouts_arr)

    if days_accounted_for == 0:
        return {
            "workouts": workouts_arr,
            "tons_lifted_avg": 0.0,
            "tons_lifted_total": 0.0,
            "calories_burned_avg": 0.0,
            "calories_burned_total": 0.0,
        }

    return {
        "workouts": workouts_arr,
        "tons_lifted_avg": round(total_tons / days_accounted_for, 2),
        "tons_lifted_total": total_tons,
        "calories_burned_avg": round(total_cals_burned / days_accounted_for, 2),
        "calories_burned_total": total_cals_burned,
    }
