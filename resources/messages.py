from flask import Blueprint, jsonify, request
import models
from playhouse.shortcuts import model_to_dict
import datetime

messages = Blueprint('messages', __name__)

@messages.route('', methods=["GET"])
def get_messages():
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
        trigger_time = datetime.datetime.now(),
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
    return jsonify(data={
        'route': 'Delete message ' + id
    }, status={
        'code': 501,
        'message': 'Not implemented'
    }), 501

