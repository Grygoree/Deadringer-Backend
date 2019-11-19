from flask import Flask
from resources.messages import messages

#TODO: Fix these for provisioning
DEBUG = True
PORT = 3000

app = Flask(__name__)

app.register_blueprint(messages, url_prefix='/api/v0/messages/')

@app.route('/')
def hello():
    return 'hi'

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)
