from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        user_message = request.json["message"]
        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are MindAlt AI, a friendly and smart assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({"reply": response.choices[0].message.content})
    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "Bir hata oluştu..."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
