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

@received.route('/<id>/readstatus', methods=["PATCH"])
@login_required
def change_status(id):
    """ Future route where user can mark a receipt as read """
    try:
        found_receipt = models.Receipt.get_by_id(id)
        if not current_user.id == found_receipt.to_user.id:
            return jsonify(data={},
                           status={
                               'code': 403,
                               'message': 'Unable to mark read on receipt with ID {}'
                           })
        else:
            found_receipt.is_read=True
            found_receipt.save()
            found_receipt_model = model_to_dict(found_receipt)
            del found_receipt_model['message']['author']['password']
            del found_receipt_model['to_user']['password']
            return jsonify(data=found_receipt_model,
                           status={
                               'code': 200,
                               'message': 'Marked read on receipt with ID {}'.format(id)
                           }),  200
    except models.DoesNotExist:
        return jsonify(data={},
                       status={
                           'code': 403,
                           'message': 'Unable to mark read on receipt with ID {}'.format(id)
                       }), 403

