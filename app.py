from flask import Flask, render_template, request, jsonify
from mindalt_ai import chat_with_mindalt_api  # MindALT AI'dan cevap döndüren fonksiyon

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get("message")
    reply = chat_with_mindalt_api(user_input)  # MindALT AI cevabı
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
