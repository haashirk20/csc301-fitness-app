import datetime


def get_last_steps(user, days):
    all_steps = user.get_steps()
    steps_arr = []
    dates_str = []
    today_date = datetime.date.today()

    # It's counting down not up to add today's date last in array for chronological order
    for i in range(days - 1, -1, -1):
        date = today_date - datetime.timedelta(days=i)
        date_str = date.isoformat()

        # if date not in all_steps:
        if date_str not in all_steps:
            dates_str.append(date_str)  # to update db with 0 steps for that date
            steps = 0
        else:
            steps = all_steps.get(date_str)

        steps_arr.append({"date": date_str, "day": date.strftime("%A"), "steps": steps})

    user.steps_reset(dates_str)

    return steps_arr
