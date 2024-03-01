from flask import request, session
from app import app
from app.models import User

@app.route('/api/profile', methods=['GET'])
def profile():
    if 'user' not in session:
        return {'message': 'user not signed in'}, 401
    
    user = User.User(id=session['user']['id'], name=session['user']['name'])
    user_profile = user.get_profile()

    # Not including sex for now
    return {'message':'success', 'name': user_profile[0], 'email': user_profile[1], 'age': str(user_profile[2])}, 200

@app.route('/api/profile', methods=['POST'])
def set_profile():
    if 'user' not in session:
        return {'message': 'user not signed in'}, 401

    data = request.get_json()
    new_name = data.get('name', '')
    new_email = data.get('email', '')
    new_age = data.get('age', '')

    user = User.User(id=session['user']['id'], name=session['user']['name'])
    user.set_profile(new_name, new_email, new_age)

    return {'message': 'success'}, 200