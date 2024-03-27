import schedule
from schedule import run_pending
import time
from app.models import User
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

SENDEMAIL = 'csc301fitnessproject@gmail.com'
SENDPWD = 'wuiu qlaf fvnn mdvb'
EMAILSUBJECTWORKOUT = 'Reminder: Workout'
EMAILTEXTWORKOUT = 'This is your scheduled daily reminder for workout.'

def check_times():
    userlist = User.User().get_all_users()
    if len(userlist) == 0:
        return None
    else:
        curr_time = datetime.now().strftime('%H:%M')
        for user in userlist:
            if "notifs" in user and "notiftime" in user["notifs"]:
                notiftime = user["notifs"]["notiftime"]
                if curr_time == notiftime:
                    WorkoutReminder(user['email'])
        return


def WorkoutReminder(email):
    smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtpserver.ehlo()
    smtpserver.login(SENDEMAIL, SENDPWD)
    msg = MIMEText(EMAILTEXTWORKOUT)
    msg['Subject'] = EMAILSUBJECTWORKOUT
    msg['From'] = SENDEMAIL
    msg['To'] = email
    smtpserver.sendmail(SENDEMAIL, email, msg.as_string())
    smtpserver.close()
    return

def reminder():
    schedule.every(1).minutes.do(check_times)
    while True:
        run_pending()
        time.sleep(1)
