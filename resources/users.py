from flask import Blueprint
import models

users = Blueprint('users', __name__)

@users.route('/', methods=['GET'])
def test_user_controller():
    return "You are not logged in"

