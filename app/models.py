from firebase_admin import db


class User:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username

    def save_to_db(self):
        ref = db.reference("users")

        new_user_ref = ref.push({"user_id": self.user_id, "username": self.username})

        return new_user_ref.key

    @staticmethod
    def get_all_users():
        ref = db.reference("users")

        users = ref.get()

        # Convert the dictionary of users to a list
        user_list = [] if users is None else list(users.values())

        return user_list
