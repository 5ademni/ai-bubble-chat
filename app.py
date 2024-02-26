from requests.exceptions import ConnectionError
from flask import Flask, request, render_template, Response
from flask_cors import CORS
from poe_api_wrapper import PoeApi
import traceback


# ------------------ SETUP ------------------


app = Flask(__name__)
client = PoeApi("CmpguqkTtuqLZh5w1XeRGw%3D%3D")
bot = "travel_assitance"

# this will need to be reconfigured before taking the app to production
cors = CORS(app)


@app.route("/")
def home():
    return render_template("index.html")


# ------------------ EXCEPTION HANDLERS ------------------

# Sends response back to Deep Chat using the Response format:
# https://deepchat.dev/docs/connect/#Response


'''@app.errorhandler(Exception)
def handle_exception(e):
    print(traceback.format_exc())
    return {"error": str(e)}, 500'''


@app.errorhandler(ConnectionError)
def handle_exception(e):
    print(e)
    return {"error": "Internal service error"}, 500

# ------------------ CUSTOM API ------------------


@app.route("/chat", methods=["POST"])
def chat():
    body = request.json
    messages = body.get('messages')
    if messages is None or len(messages) == 0:
        return {"error": "No message provided"}, 400
    message = messages[0].get('text')
    print(f"Received message: {message}")  # print the received message
    if message is None:
        return {"error": "No message provided"}, 400
    message = str(message)  # convert message to string
    chunks = []
    for chunk in client.send_message(bot, message):
        pass
    print(chunk["text"])
    return {"text": chunk["text"]}


@app.route("/chat-stream", methods=["POST"])
def chat_stream():
    body = request.json
    message = body.get('message')
    print(f"Received message: {message}")  # print the received message

    def generate():
        for chunk in client.send_message(bot, message):
            yield chunk["response"]
    return Response(generate(), mimetype='text/plain')


if __name__ == "__main__":
    app.run(port=8080)
