from flask import Flask, g
from resources.messages import messages
from resources.users import users
import models

#TODO: Fix these for provisioning
DEBUG = True
PORT = 3000

app = Flask(__name__)

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
