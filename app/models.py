from app import bcrypt
from firebase_admin import db


class User:
    def __init__(self, email, hash):
        self.email = email
        self.hash = bcrypt.generate_password_hash(hash, 10)

    def save_to_db(self):
        ref = db.reference("users")
        new_user_ref = ref.push({"email": self.email, "hash": self.hash})

        return new_user_ref.key

    def get_email(self):
        return self.email

    @staticmethod
    def login(form_email, form_pass):
        ref = db.reference("users")
        user_dict = ref.order_by_child("email").equal_to(form_email).get()
        user = next(iter(user_dict.items()), None)

        if user:
            # user found, get their email/hash
            user_id = user[0]
            user_hash = user[1]["hash"]
            form_hash = bcrypt.generate_password_hash(form_pass, 10)
            if user_hash == form_hash:
                return user_id
        else:
            return None

    @staticmethod
    def get_all_users():
        ref = db.reference("users")

        users = ref.get()

        # Convert the dictionary of users to a list
        user_list = [] if users is None else list(users.values())

        return user_list
