from flask import Blueprint
import models

received = Blueprint('received', __name__)

@received.route('/', methods=["GET"])
def get_inbox():
    """ Only returns messages whose trigger date is now """
    return "hitting inbox route"

@received.route('/<id>', methods=["PUT"])
def change_status(id):
    """ Future route where user can mark a message as read """
    return "Updating message with id {}".format(id)

