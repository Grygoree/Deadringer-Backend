from flask import Flask, g, jsonify
from resources.messages import messages
from resources.users import users
import models
from flask_login import LoginManager
from flask_cors import CORS

#TODO: Fix these for provisioning
DEBUG = True
PORT = 3000
ALLOWED_CORS_CLIENTS = ['http://localhost:3001']

app = Flask(__name__)

#TODO: Provision this as well
#Session management
app.secret_key = b'Thisshoudlntbehere\xecffwww3##_'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get_by_id(user_id)
    except:
        return None

@login_manager.unauthorized_handler
def send_unauth():
    return jsonify(
        data={},
        status={
            'code': 401,
            'message': 'You must be logged in to access that resource.'
        }), 401

CORS(users, origins=ALLOWED_CORS_CLIENTS, supports_credentials=True)
CORS(messages, origins=ALLOWED_CORS_CLIENTS, supports_credentials=True)

app.register_blueprint(messages, url_prefix='/api/v0/messages')
app.register_blueprint(users, url_prefix='/api/v0/users')

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    g.db = models.DATABASE
    g.db.close()
    return response

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
