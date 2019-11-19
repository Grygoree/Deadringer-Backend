from flask import Flask

#TODO: Fix these for provisioning
DEBUG = True
PORT = 3000

app = Flask(__name__)

@app.route('/')
def hello():
    return 'hi'

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)
