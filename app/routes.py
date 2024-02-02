from app import app


@app.route("/hello")
def home():
    user = get_authenticated_user()
    if user:
        return f"Hey, {user['email']}! You are authenticated."
    else:
        return "Hey, anonymous user! You are not authenticated."


def get_authenticated_user():
    # Implement the logic to check authentication
    # ...
    pass
