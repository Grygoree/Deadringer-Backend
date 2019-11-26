from flask import Blueprint, jsonify
import models
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict
import datetime

received = Blueprint('received', __name__)

@received.route('/', methods=["GET"])
@login_required
def get_inbox():
    """ Only returns messages whose trigger date is now """
    try:
        #This query gives the messages that a user has actually received
        triggered_messages = (models
        .User
        .get_by_id(current_user.id)
        .received_messages
        .join(models.Message)
        .select()
        .where(models.Message.trigger_time < datetime.datetime.now()))

        received_messages_dicts = [model_to_dict(m) for m in triggered_messages]
        #Scrub passwords
        for m in received_messages_dicts:
            del m['message']['author']['password']
            del m['to_user']['password']
        return jsonify(data=received_messages_dicts,
                       status={
                           'code': 200,
                           'message': 'Successfully retrieved received messages'
                       }), 200
    except models.DoesNotExist:
        return jsonify(data={},
                       status={
                           'code': 500,
                           'message': 'Unable to retrieve received messages'
                       }), 500

@received.route('/<id>', methods=["PUT"])
def change_status(id):
    """ Future route where user can mark a message as read """
    return jsonify(data={},
                   status={
                       'code': 501,
                       'message': 'Not implemented'
                   }), 501

