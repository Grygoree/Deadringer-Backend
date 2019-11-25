from flask import Blueprint, jsonify, request
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
import models
from playhouse.shortcuts import model_to_dict

users = Blueprint('users', __name__)

@users.route('/', methods=['GET'])
def test_user_controller():
    if current_user.is_authenticated:
        return jsonify(
            data={},
            status = {
                'code': 200,
                'message': "You are logged in as {}".format(current_user.email)
            }
        ), 200
    else:
        return jsonify(
            data={},
            status={
                'code': 401,
                'message': "No user is logged in."
            }
        ), 401


@users.route('/register', methods=["POST"])
def register():
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
        del user_dict['password']
        return jsonify(data=user_dict, status={
            'code': 201,
            'message': 'Successfully registered {}'.format(user_email)
        }), 201

@users.route('/login', methods=["POST"])
def login():
    payload = request.get_json()
    user_email = payload['email'].lower()
    try:
        found_user = models.User.get(models.User.email == user_email)
        hashed_pass = found_user.password
        password_does_match = check_password_hash(hashed_pass, payload['password'])
        if (password_does_match):
            login_user(found_user)
            return jsonify(data={'email': found_user.email}, status={
                'code': 200,
                'message': 'Logged in successfully as {}'.format(user_email)
            }), 200
        else:
            return jsonify(data={}, status={
                'code': 401,
                'message': 'Failed to log in. Email does not exist or password incorrect.'
            }), 401
    except models.DoesNotExist:
        return jsonify(data={}, status={
            'code': 401,
            'message': 'Failed to log in. Email does not exist or password incorrect.'
        }), 401

@users.route('/logout', methods=["GET"])
def logout():
    logout_message = 'Logged out of no user'
    if current_user.is_authenticated:
        logout_message = 'Logged out of {}'.format(current_user.email)
        logout_user()
    return jsonify(data={}, status={
        'code': 200,
        'message': logout_message
    }), 200
