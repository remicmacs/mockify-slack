from flask import Flask, jsonify, request
from mockify import mockify

app = Flask(__name__)

@app.route("/")
def hello():
    '''
    Root endpoint, maybe to show a howto ?
    '''
    return jsonify(mockify("Hello, world"))

@app.route("/api/mockify/")
def spongebobcase():
    '''
    Retrieve a GET HTTP request with a `mockify` parameter and returns the
    string mocked like in the Mocking SpongeBob meme
    '''

    app.logger.info("/api/mockify endpoint reached")
    s = request.args.get("mockify", 0, type=str)
    app.logger.debug("string retrieved : \'" + s + "\'")

    return jsonify(mockify(s))



