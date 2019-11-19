from flask import Blueprint, jsonify

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
    return jsonify(data={
        'route': 'Create message'
    }, status={
        'code': 501,
        'message': 'Not implemented'
    }), 501

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

