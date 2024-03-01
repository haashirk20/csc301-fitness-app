import os
import flask
import firebase_admin
from firebase_admin import credentials
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from threading import Thread
from utils import reminders
app = flask.Flask(__name__)

app.config.update(
    SESSION_COOKIE_SECURE="False",
    SESSION_COOKIE_SAMESITE="None",
)
CORS(
    app,
    # below is the front end url
    origins=["http://127.0.0.1:5500, http://127.0.0.1:5501"],
    supports_credentials=True,
)

SECRET_KEY = "batman"  # TODO: put in .env file
app.secret_key = SECRET_KEY
bcrypt = Bcrypt(app)

FIREBASE_ADMIN_KEY_PATH = os.path.join(
    os.getcwd(), "csc301-fitness-app-firebase-admin-1.json"
)


def initialize_firebase_app():
    if not firebase_admin._apps:
        cred = credentials.Certificate(FIREBASE_ADMIN_KEY_PATH)
        firebase_admin.initialize_app(
            cred,
            {"databaseURL": "https://csc301-fitness-app-default-rtdb.firebaseio.com/"},
        )


initialize_firebase_app()

thread = Thread(target=reminders.Reminder())
thread.start()
thread.join()

from app import routes  # placed down here to avoid circular imports
