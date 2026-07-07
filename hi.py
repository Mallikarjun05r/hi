import os
import socket

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


def find_available_port(start_port):
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("127.0.0.1", port))
                return port
            except OSError:
                port += 1


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/greet", methods=["POST"])
def greet():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()

    if not name:
        return jsonify({"message": "Please enter your name."}), 400

    return jsonify({"message": f"Welcome, {name}!"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5001"))
    app.run(debug=True, host="127.0.0.1", port=find_available_port(port), use_reloader=False)