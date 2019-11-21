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
            'route': 'Index messages'
        }, status={
            'code': 501,
            'message': 'Not implemented'
        }), 501

@messages.route('', methods=["POST"])
def create_message():
    payload = request.get_json()

    message = models.Message.create(
        author = 1,#current_user.id
        body =  payload['body'],
        trigger_time = datetime.datetime.now() + datetime.timedelta(days=1),
    )

    for recipient in payload['recipients']:
        print(recipient)
        #create a receipt

    message_dict = model_to_dict(message)
    message_dict['author'].pop('password')

    return jsonify(
        data=message_dict,
        status={
            'code': 201,
            'message': 'Sucessfully created a message'
        }), 201

@messages.route('<id>', methods=["PUT"])
def update_message(id):
    return jsonify(data={
        'route': 'Update message ' + id
    }, status={
        'code': 501,
        'message': 'Not implemented'
    }), 501

@messages.route('<id>', methods=["DELETE"])
def delete_message(id):
    try:
        message = models.Message.get_by_id(id)
        if message.author.id != 1: #current_user.id
            return jsonify(
                data={},
                status={
                    'code': 403,
                    'message': 'User can only delete their own messages or message does not exist'
                })
        else:
            message.delete_instance()
            message_dict = model_to_dict(message)
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
