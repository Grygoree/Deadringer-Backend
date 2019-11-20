from flask import Blueprint, jsonify, request
import models

users = Blueprint('users', __name__)

@users.route('/', methods=['GET'])
def test_user_controller():
    return "You are not logged in"

@users.route('/register', methods=["POST"])
def register_user():
    #see if email taken and pword valid
    payload = request.get_json()
    user_email = payload['email'].lower()
    payload['email'] = user_email
    try:
        models.User.get(models.User.email == user_email)
        return jsonify(data={}, status={
            'code': 401,
            'message': 'The email {} is taken or reserved.'.format(user_email)
        }), 401
    except models.DoesNotExist:
        #models.User.create(**payload)
        return jsonify(data={}, status={
            'code': 201,
            'message': 'Successfully registered {}'.format(user_email)
        }), 201

@users.route('/login', methods=["POST"])
def login_user():
    #see if email exists and pword valid
    return jsonify({'status': 'login'})

@users.route('/logout', methods=["POST"])
def logout_user():
    #clear session
    return jsonify({'status': 'logout'})
