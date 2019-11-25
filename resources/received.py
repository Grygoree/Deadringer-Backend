from flask import Blueprint, jsonify
import models
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict

received = Blueprint('received', __name__)

@received.route('', methods=["GET"])
@login_required
def get_inbox():
    """ Only returns messages whose trigger date is now """
    try:
        found_user = models.User.get_by_id(current_user.id)
        received_messages_dicts = [model_to_dict(m) for m in found_user.received_messages]
        for m in received_messages_dicts:
            #Scrub passwords
            del m['message']['author']['password']
            del m['to_user']['password']
        return jsonify(data=received_messages_dicts), 200
    except models.DoesNotExist:
        return "something went wrong"
    return "hitting inbox route"

@received.route('/<id>', methods=["PUT"])
def change_status(id):
    """ Future route where user can mark a message as read """
    return "Updating message with id {}".format(id)

