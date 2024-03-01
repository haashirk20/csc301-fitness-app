import datetime


def previous_sleeps(user, days):
    sleep_records = user.get_sleep_records()
    sleep_arr = []
    today_date = datetime.date.today()
    total_hours = 0.0
    days_accounted_for = 0

    # It's counting down not up to add today's date last in array for chronological order
    for i in range(days - 1, -1, -1):
        date = today_date - datetime.timedelta(days=i + 1)
        date_str = date.isoformat()

        # if user didn't record sleep for that day:
        if date_str not in sleep_records:
            sleep_record = None
        else:
            sleep_record = sleep_records.get(date_str)
            days_accounted_for += 1
            total_hours += sleep_record

        sleep_arr.append(
            {"date": date_str, "day": date.strftime("%A"), "hours": sleep_record}
        )

    if days_accounted_for == 0:
        return {
            "sleep": sleep_arr,
            "hours_avg": 0.0,
            "hours_total": 0.0,
        }

    hours_avg = total_hours / days_accounted_for

    return {
        "sleep": sleep_arr,
        "hours_avg": hours_avg,
        "hours_total": total_hours,
    }
