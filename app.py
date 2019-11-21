from flask import Flask, g
from resources.messages import messages
from resources.users import users
import models
from flask_login import LoginManager

#TODO: Fix these for provisioning
DEBUG = True
PORT = 3000

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
