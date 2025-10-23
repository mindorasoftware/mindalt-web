# app.py
from flask import Flask, request, jsonify, render_template
import os
from mindalt_ai import chat_with_mindalt_api

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")  # templates/index.html kullanılacak

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message")
    if not user_input:
        return jsonify({"error": "Mesaj boş olamaz."}), 400
    response = chat_with_mindalt_api(user_input)
    return jsonify({"reply": response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render için dinamik port
    app.run(host="0.0.0.0", port=port)
