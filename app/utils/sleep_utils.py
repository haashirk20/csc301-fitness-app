import datetime


def previous_sleeps(user, days):
    sleep_records = user.get_sleep_records()
    sleep_arr = []
    today_date = datetime.date.today()
    total_hours = 0
    total_minutes = 0
    days_accounted_for = 0

    # It's counting down not up to add today's date last in array for chronological order
    for i in range(days - 1, -1, -1):
        date = today_date - datetime.timedelta(days=i + 1)
        date_str = date.isoformat()

        # if user didn't record sleep for that day:
        if date_str not in sleep_records:
            sleep_record = {"hours": None, "minutes": None}
        else:
            sleep_record = sleep_records.get(date_str)
            days_accounted_for += 1
            total_hours += sleep_record["hours"]
            total_minutes += sleep_record["minutes"]

        sleep_arr.append(
            {
                "date": date_str,
                "hours": sleep_record["hours"],
                "minutes": sleep_record["minutes"],
            }
        )

    total_minutes = (total_hours * 60 + total_minutes) // days_accounted_for
    hours = total_minutes // 60
    minutes = total_minutes % 60

    return {
        "sleep": sleep_arr,
        "hours_avg": hours,
        "minutes_avg": minutes,
    }
