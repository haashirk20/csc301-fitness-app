from app import bcrypt
from firebase_admin import db
import json


class User:
    def __init__(self, id=0, name="", password="", email="", age=0):
        self.id = id  # firebase id
        self.name = name
        self.age = age
        self.email = email
        self.password = password
        if len(self.password) > 0:
            self.hash = bcrypt.generate_password_hash(password, 10).decode()

    def signup(self):
        ref = db.reference("users")
        # user must be unique
        user_dict = ref.order_by_child("name").equal_to(self.name).get()
        if len(user_dict) == 0:
            new_user_ref = ref.push(
                {
                    "email": self.email,
                    "hash": self.hash,
                    "age": self.age,
                    "name": self.name,
                }
            )
            return True
        else:
            return False

    # checks whether user exists and password is correct
    # returns True on success, False on failure
    def login(self):
        ref = db.reference("users")
        user_dict = ref.order_by_child("name").equal_to(self.name).get()
        user = next(iter(user_dict.items()), None)

        if user and bcrypt.check_password_hash(user[1]["hash"], self.password):
            self.id = user[0]
            self.name = user[1]["name"]
            self.email = user[1]["email"]
            self.hash = user[1]["hash"]
            return True
        else:
            return False

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_age(self):
        return self.age

    @staticmethod
    def get_all_users():
        ref = db.reference("users")

        users = ref.get()

        user_list = [] if users is None else list(users.values())

        return user_list
