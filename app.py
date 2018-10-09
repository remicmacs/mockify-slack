import requests
from flask import Flask, jsonify, request
from mockify import mockify
from functools import wraps

app = Flask(__name__)

blacklist = [
    "U7D2XEMEC", # Gwendal
    "U9A5V02AW", # Nelson (do NOT remove)
    # "U7EG16H3R", # Vincent
    # "U7DNH2BUJ", # Rodolphe
    "U7DDC77SP", # Rémi
]

def get_current_user_id(req):
    return req.form["user_id"]

def access_locked_response(req):
    return jsonify(mockify(
        "I'm sorry " + request.form["user_name"].split('.')[0]
        + ", I'm afraid I can't do that"
        )
    )

def requires_access_rights(*access_rights):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if get_current_user_id(request) not in access_rights:
                return access_locked_response(request)
            return f(*args, **kwargs)
        return wrapped
    return wrapper

def log(req):
    app.logger.info(
        "/api/mockifyapp/ endpoint reached by \""
        + "{:<25}".format(req.form["user_name"]) + "\", user_id: \""
        + "{:9}".format(req.form["user_id"]) + "\""
        + "; message: \"" + "{:<50}".format(req.form["text"]) + "\""
        + " ; in channel \"" + "{:<20}".format(req.form["channel_name"])
        + "\", channel_id: \"" + "{:9}".format(req.form["channel_id"]) + "\""
    )

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
@requires_access_rights(blacklist)
def slackmock():
    '''
    Retrieve a POST HTTP request from Slack and mockify the text passed as
    parameter in the request.form["text"]
    '''
    # Logging incoming request
    log(request)

    # Forging request for delayed response
    req_payload = {
        "response_type": "in_channel",
        "text": mockify(request.form["text"])
    }
    # Sending request to response_url sent by slack slash command
    requests.post(request.form["response_url"], json=req_payload)

    # Return 200 status to HTTP request (ack)
    return ""

@app.route("/api/mockifyapp/bot/", methods=["POST"])
def slack_mock_bot():
    app.logger.info("/api/mockifyapp/bot/ endpoint reached")
    app.logger.info(request.data["challenge"])
    challenge = request.form["challenge"]
    app.logger.info("Challenge retrieved: ")
    app.logger.info(challenge)
    return jsonify({"challenge": request.form["challenge"]})
