import os
import flask
import firebase_admin
from firebase_admin import credentials, db

app = flask.Flask(__name__)


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

from app import models, routes  # placed here to avoid circular imports
