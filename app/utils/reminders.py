import schedule
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
            if curr_time == user['notiftime']:
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


def Reminder():
    schedule.every(15).minutes.do(check_times())
    while True:
        schedule.run_pending()
        time.sleep(1)

