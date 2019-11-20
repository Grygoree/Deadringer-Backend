from flask import Blueprint, jsonify, request
from flask_bcrypt import generate_password_hash, check_password_hash
import models
from playhouse.shortcuts import model_to_dict

users = Blueprint('users', __name__)

@users.route('/', methods=['GET'])
def test_user_controller():
    return "You are not logged in"

@users.route('/register', methods=["POST"])
def register_user():
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
        hashed_pass = generate_password_hash(payload['password'])
        payload['password'] = hashed_pass
        created_user = models.User.create(**payload)
        user_dict = model_to_dict(created_user)
        return jsonify(data=user_dict, status={
            'code': 201,
            'message': 'Successfully registered {}'.format(user_email)
        }), 201

@users.route('/login', methods=["POST"])
def login_user():
    payload = request.get_json()
    user_email = payload['email'].lower()
    try:
        found_user = models.User.get(models.User.email == user_email)
        hashed_pass = found_user.password
        password_does_match = check_password_hash(hashed_pass, payload['password'])
        if (password_does_match):
            print('good password')
        else:
            print('bad password')
        return jsonify(data={}, status={
            'code': 401,
            'message': 'Failed to log in. Email does not exist or password incorrect.'
        }), 401
    except models.DoesNotExist:
        return jsonify(data={}, status={
            'code': 401,
            'message': 'Failed to log in. Email does not exist or password incorrect.'
        }), 401

@users.route('/logout', methods=["POST"])
def logout_user():
    #clear session
    return jsonify({'status': 'logout'})
