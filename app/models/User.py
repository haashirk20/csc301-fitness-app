from app import bcrypt
from firebase_admin import db
import datetime
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
        self.calories_needed = 0
        self.calories_remaining = 0
        self.sex = ""

    def signup(self):
        ref = db.reference("users")
        # user must be unique
        user_dict = ref.order_by_child("name").equal_to(self.name).get()
        if len(user_dict) == 0:
            new_user_ref = ref.push(
                {
                    "email": self.email,
                    "hash": self.hash,
                    "age": int(self.age),
                    "name": self.name,
                    "calories_needed": self.calories_needed,
                    "calories_remaining": self.calories_remaining,
                    "sleep": {"goal": 0, "records": {}},
                    "steps": {},
                    "notifs": {"notiftime": ""},
                    "workouts": {},
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

    def get_profile(self):
        user_ref = db.reference("users").child(self.id)
        user = user_ref.get()
        self.name = user.get("name")
        self.email = user.get("email")
        self.age = user.get("age")

        return self.name, self.email, self.age, self.sex

    def set_profile(self, name, email, age, sex):
        user_ref = db.reference("users").child(self.id)
        # if name, email, age or sex is empty, do not update
        if name:
            user_ref.update({"name": name})
            self.name = name
        if email:
            user_ref.update({"email": email})
            self.email = email
        if age:
            user_ref.update({"age": int(age)})
            self.age = int(age)
        # if sex:
        #     user_ref.update({"sex": sex})

    def set_calories(self, calories):
        user_ref = db.reference("users").child(self.id)
        user_ref.update({"calories_needed": calories, "calories_remaining": calories})
        self.calories_needed = calories
        self.calories_remaining = calories

    def calories_reduce(self, calories_used):
        user_ref = db.reference("users").child(self.id)
        calories_remaining = user_ref.get().get("calories_remaining") - calories_used
        user_ref.update({"calories_remaining": calories_remaining})
        self.calories_remaining = calories_remaining

    def calories_reset(self):
        user_ref = db.reference("users").child(self.id)
        caloried_needed = user_ref.get().get("calories_needed")
        user_ref.update({"calories_remaining": caloried_needed})
        self.calories_needed = caloried_needed
        self.calories_remaining = caloried_needed

    def set_sleep_goal(self, goal):
        user_ref = db.reference("users").child(self.id).child("sleep")
        sleep_obj = user_ref.get()
        sleep_obj["goal"] = goal
        user_ref.update(sleep_obj)
        print("set", sleep_obj["goal"])
        return sleep_obj["goal"]

    def set_sleep_record(self, date_slept, hours):
        user_ref = db.reference("users").child(self.id).child("sleep")
        sleep_obj = user_ref.get() or {}
        sleep_obj.setdefault("records", {})
        sleep_obj["records"][str(date_slept)] = hours
        user_ref.update(sleep_obj)
        return sleep_obj["records"][str(date_slept)]

    def get_sleep_records(self):
        user_ref = db.reference("users").child(self.id).child("sleep")
        sleep_obj = user_ref.get()
        return sleep_obj.get("records") or {}

    def get_sleep_goal(self):
        user_ref = db.reference("users").child(self.id).child("sleep")
        sleep_obj = user_ref.get()
        return sleep_obj.get("goal")

    def steps_add(self, steps, date_str="today"):
        if date_str == "today":
            date_str = datetime.date.today().isoformat()

        user_ref = db.reference("users").child(self.id).child("steps")
        steps_obj = user_ref.get()
        updated_steps = steps_obj.get(date_str, 0) + steps
        steps_obj[date_str] = updated_steps
        user_ref.set(steps_obj)

        return updated_steps

    def steps_reset(self, dates_str):
        user_ref = db.reference("users").child(self.id).child("steps")
        steps_obj = user_ref.get() or {}
        for date_str in dates_str:
            steps_obj[date_str] = 0
        user_ref.set(steps_obj)

        return 0

    def set_notifs(self, notif_time):
        print("SD", notif_time)
        user_ref = db.reference("users").child(self.id).child("notifs")
        notif_obj = user_ref.get() or {}
        print("get", notif_obj)
        notif_obj["notiftime"] = notif_time
        user_ref.update(notif_obj)
        print("set", notif_obj["notiftime"])
        return notif_obj["notiftime"]

    def set_workout_record(self, today_date, tonnage, cals):
        user_ref = db.reference("users").child(self.id).child("workouts")
        workouts_obj = user_ref.get() or {}
        new_total_tonnage = workouts_obj.get(today_date, {}).get("tonnage", 0) + tonnage
        new_total_cals = workouts_obj.get(today_date, {}).get("calories", 0) + cals

        workouts_obj[today_date] = {
            "tonnage": round(new_total_tonnage, 2),
            "calories": round(new_total_cals, 2),
        }
        user_ref.update(workouts_obj)
        return workouts_obj[str(today_date)]

    def get_workout_records(self):
        workout_obj = db.reference("users").child(self.id).get().get("workouts", {})
        return workout_obj

    def get_steps(self):
        steps_obj = db.reference("users").child(self.id).get().get("steps", {})
        return steps_obj

    def get_calories_needed(self):
        self.calories_needed = (
            db.reference("users").child(self.id).get()["calories_needed"]
        )
        return self.calories_needed

    def get_calories_remaining(self):
        self.calories_remaining = (
            db.reference("users").child(self.id).get()["calories_remaining"]
        )
        return self.calories_remaining

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
