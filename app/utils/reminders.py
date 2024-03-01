import schedule
import time
from app.models import User
import smtplib
from email.mime.text import MIMEText

SENDEMAIL = 'csc301fitnessproject@gmail.com'
SENDPWD = 'wuiu qlaf fvnn mdvb'
EMAILSUBJECTSLEEP = 'Reminder: Sleep'
EMAILSUBJECTWORKOUT = 'Reminder: Workout'
EMAILTEXTSLEEP = 'This is your scheduled daily reminder for sleep.'
EMAILTEXTWORKOUT = 'This is your scheduled daily reminder for workout.'

def SleepReminder():
    userlist = User.User().get_all_users()
    if len(userlist) == 0:
        return None
    else:
        smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtpserver.ehlo()
        smtpserver.login(SENDEMAIL, SENDPWD)
        for user in userlist:
            useremail = user["email"]
            msg = MIMEText(EMAILTEXTSLEEP)
            msg['Subject'] = EMAILSUBJECTSLEEP
            msg['From'] = SENDEMAIL
            msg['To'] = useremail
            smtpserver.sendmail(SENDEMAIL, useremail, msg.as_string())
        smtpserver.close()


def WorkoutReminder():
    userlist = User.User().get_all_users()
    if len(userlist) == 0:
        return None
    else:
        smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtpserver.ehlo()
        smtpserver.login(SENDEMAIL, SENDPWD)
        for user in userlist:
            useremail = user["email"]
            msg = MIMEText(EMAILTEXTWORKOUT)
            msg['Subject'] = EMAILSUBJECTWORKOUT
            msg['From'] = SENDEMAIL
            msg['To'] = useremail
            smtpserver.sendmail(SENDEMAIL, useremail, msg.as_string())
        smtpserver.close()


def Reminder():
    schedule.every().day.at("22:00").do(SleepReminder())
    schedule.every().day.at("11:20").do(WorkoutReminder())
    while True:
        schedule.run_pending()
        time.sleep(1)

