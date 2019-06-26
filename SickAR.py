from flask import Flask, make_response
import requests

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/tamper')
def tamper():

    return True


if __name__ == '__main__':
    # print(__name__)
    app.run(debug=True)
