from flask import Blueprint, jsonify

messages = Blueprint('messages', __name__)

@messages.route('', methods=["GET"])
def get_messages():
    return jsonify(data={
        #Data here
    }, status={
        'code': 501, 
        'message': 'Not implemented'
    }), 501


