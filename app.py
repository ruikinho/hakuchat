import os

from flask import Flask, render_template, request, jsonify

from chat_core import ask_chat

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "")
    history = data.get("history", [])

    if not isinstance(history, list):
        history = []

    messages = [*history, {"role": "user", "content": user_message}]

    response_text, searches_used = ask_chat(messages)

    return jsonify({
        "response": response_text,
        "searches_used": searches_used,
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
