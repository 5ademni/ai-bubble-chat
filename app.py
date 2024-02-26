from requests.exceptions import ConnectionError
from custom import Custom
from flask import Flask, request, render_template
from flask_cors import CORS

# ------------------ SETUP ------------------


app = Flask(__name__)

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
    print(e)
    return {"error": str(e)}, 500


@app.errorhandler(ConnectionError)
def handle_exception(e):
    print(e)
    return {"error": "Internal service error"}, 500

# ------------------ CUSTOM API ------------------


custom = Custom()


@app.route("/chat", methods=["POST"])
def chat():
    body = request.json
    return custom.chat(body)


@app.route("/chat-stream", methods=["POST"])
def chat_stream():
    body = request.json
    return custom.chat_stream(body)


@app.route("/files", methods=["POST"])
def files():
    return custom.files(request)


if __name__ == "__main__":
    app.run(port=8080)
