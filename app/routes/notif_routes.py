from flask import request, session
from app import app
from app.models import User
from datetime import datetime

@app.route('/api/notifications', methods=['POST'])
def set_notifs():
    if "user" not in session:
        return {'message': 'user not signed in'}, 401

    data = request.get_json()
    new_notif = data.get("newTime", "")

    user = User.User(id=session["user"]["id"])
    time = user.set_notifs(new_notif)
    time_value = datetime.strptime(time, "%H:%M")
    time_12hour = time_value.strftime("%I:%M%p")
    return {'time': time_12hour}, 200

