from flask import Flask, jsonify, request
from api.API import send_message_discord, create_object
from Config import getPyPort

app = Flask(__name__)


@app.route("/sendmessage", methods=["POST"])
def sendmessage():
    new_item = request.json
    send_message_discord(create_object(message=new_item["message"], name=new_item["name"]))
    return jsonify(new_item), 201


def flask_run():
    app.run(debug=False, port=getPyPort())
