from flask import request, session
from app import app
from app.models import User

@app.route('/api/notifs', methods=['POST'])
def set_profile():
    if "user" not in session:
        return {'message': 'user not signed in'}, 401

    data = request.get_json()
    new_notif = data.get('notiftime', '')

    user = User.User(id=session['user']['id'], name=session['user']['name'])
    user.set_notifs(new_notif)

    return {'message': 'success'}, 200
