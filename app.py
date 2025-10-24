from flask import Flask, request, jsonify
from flask_cors import CORS  # CORS için
import openai
import os

app = Flask(__name__)
CORS(app)  # Bu satır tüm domainlerden istek kabul eder

# OpenAI API key'i environment variable olarak ayarla
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/api", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")
        if not user_message:
            return jsonify({"error": "Mesaj boş"}), 400

        # OpenAI çağrısı
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sen bir yardımcı asistanın."},
                {"role": "user", "content": user_message}
            ]
        )

        answer = response['choices'][0]['message']['content']
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Render port kullanımı için
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
