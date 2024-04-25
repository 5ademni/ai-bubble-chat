from requests.exceptions import ConnectionError
from flask import Flask, request, render_template, Response, stream_with_context
from flask_cors import CORS
from poe_api_wrapper import PoeApi
import traceback


# ------------------ SETUP ------------------


app = Flask(__name__)
tokens = {
    'b': 'YVNKZKBGPbWgKMAW1Xn17g%3D%3D',
    'lat': 'qf2oLEe0K1aw4G2NxfvwsaN9b9no9%2BsjrhlXsDWqHA%3D%3D'
}

client = PoeApi(cookie=tokens)
bot = "5ademni_bot"

# this will need to be reconfigured before taking the app to production
cors = CORS(app)


@app.route("/")
def home():
    return render_template("index.html")


# ------------------ EXCEPTION HANDLERS ------------------

# Sends response back to Deep Chat using the Response format:
# https://deepchat.dev/docs/connect/#Response


@app.errorhandler(Exception)
def handle_exception(e):
    print(traceback.format_exc())
    return {"error": str(e)}, 500

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
    for chunk in client.send_message(bot, message):
        pass
    # DEBUG print(chunk["text"])
    return {"text": chunk["text"]}


@app.route("/chat-stream", methods=["POST"])
def chat_stream():
    messages = body.get('messages')
    if messages is None or len(messages) == 0:
        return {"error": "No message provided"}, 400
    message = messages[0].get('text')
    print(f"Received message: {message}")  # print the received message
    if message is None:
        return {"error": "No message provided"}, 400
    message = str(message)  # convert message to string

    def generate():
        for chunk in client.send_message(bot, message):
            print(chunk["response"], end="", flush=True)
            yield chunk["response"] + "\n"

    return Response(stream_with_context(generate()), mimetype='text/plain')


if __name__ == "__main__":
    app.run(port=7890)
