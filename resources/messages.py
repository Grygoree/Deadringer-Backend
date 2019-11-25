from flask import Blueprint, jsonify, request
import models
from playhouse.shortcuts import model_to_dict
import datetime
from flask_login import login_required, current_user

messages = Blueprint('messages', __name__)

@messages.route('', methods=["GET"])
@login_required
def get_messages():
    try:
        users_messages = models.Message.select().where(
            models.Message.author_id == current_user.id
        )
        message_dicts = [model_to_dict(m) for m in users_messages]
        for m in message_dicts:
            m['author'].pop('password')

        return jsonify(
            data=message_dicts,
            status={
                'code': 200,
                'message': 'Successfully retrieved created messages'
            }
        ), 200
    except models.DoesNotExist:
        return jsonify(data={
        }, status={
            'code': 500,
            'message': 'Unable to retrieve messages'
        }), 500

@messages.route('', methods=["POST"])
@login_required
def create_message():
    payload = request.get_json()

    message = models.Message.create(
        author = current_user.id,
        body = payload['body'],
        trigger_time = datetime.datetime.now() + datetime.timedelta(minutes=120),
    )

    #Make a Receipt for each existant email address in the request
    #Silently don't create a receipt if email does not exist
    for to_email in payload['recipients']:
        try:
            found_recipient = models.User.get(models.User.email == to_email)
            models.Receipt.create(to_user=found_recipient, message=message)
        except models.DoesNotExist:
            pass

    #Give a success response with removed password
    message_dict = model_to_dict(message)
    message_dict['author'].pop('password')
    return jsonify(
        data=message_dict,
        status={
            'code': 201,
            'message': 'Sucessfully created a message'
        }), 201

@messages.route('<id>', methods=["PUT"])
@login_required
def update_message(id):
    try:
        message = models.Message.get_by_id(id)
        if not message.author.id == current_user.id:
            return jsonify(
                data={},
                status={
                    'code': 403,
                    'message': 'User can only update their own messages or message does not exist'
                })
        else:
            payload = request.get_json()
            message.body = payload['body'] if 'body' in payload else None
            #TODO: figure out a good way to edit dates
            #message.trigger_time = payload['trigger_time'] if 'trigger_time' in payload else None
            #TODO: figure out a good way to edit recipients
            message.save()

            message_dict = model_to_dict(message)
            message_dict['author'].pop('password')
            return jsonify(
                data=message_dict,
                status={
                    'code': 200,
                    'message': 'Successfully updated message'
                })
    except models.DoesNotExist:
        return jsonify(
            data={},
            status={
                'code': 403,
                'message': 'User can only update their own messages or message does not exist'
            })

@messages.route('<id>', methods=["DELETE"])
@login_required
def delete_message(id):
    try:
        message = models.Message.get_by_id(id)
        if not message.author.id == current_user.id:
            return jsonify(
                data={},
                status={
                    'code': 403,
                    'message': 'User can only delete their own messages or message does not exist'
                })
        else:
            message.delete_instance()
            message_dict = model_to_dict(message)
            message_dict['author'].pop('password')
            return jsonify(
                data=message_dict,
                status={
                    'code': 200,
                    'message': 'Successfully deleted message'
                })
    except models.DoesNotExist:
        return jsonify(
            data={},
            status={
                'code': 403,
                'message': 'User can only delete their own messages or message does not exist'
            })
