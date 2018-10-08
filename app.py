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

@app.route("/api/mockifyapp/", methods=["POST"])
def slackmock():
    '''
    Retrieve a POST HTTP request from Slack and mockify the text passed as
    parameter in the request.form["text"]
    '''
    blacklist = [
        "U7D2XEMEC", # Gwendal
        "U9A5V02AW", # Nelson (do NOT remove)
    ]

    # Filter blacklist
    if (request.form["user_id"] in blacklist):
        return jsonify(mockify(
            "I'm sorry " + request.form["user_name"].split('.')[0]
            + ", I'm afraid I can't do that"
            ))

    app.logger.info('/api/mockifyapp/ endpoint reached')
    app.logger.debug('Text payload: ' + request.form["text"])
    app.logger.debug('User_id' + request.form["user_id"])

    # Forging request for delayed response
    req_payload = {
        "response_type": "in_channel",
        "text": mockify(request.form["text"])
    }
    # Sending request to response_url sent by slack slash command
    requests.post(request.form["response_url"], json=req_payload)

    # Return 200 status to HTTP request (ack)
    return ""
