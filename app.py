from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import sys

# Mevcut dizini Python path'e ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# mindalt_ai modülünü import et
try:
    from mindalt_ai import get_response
    print("✓ mindalt_ai modülü başarıyla yüklendi!")
except ImportError as e:
    print(f"✗ mindalt_ai import hatası: {e}")
    # Alternatif import yöntemi
    import importlib.util
    spec = importlib.util.spec_from_file_location("mindalt_ai", "mindalt_ai.py")
    mindalt_ai = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mindalt_ai)
    get_response = mindalt_ai.get_response

app = Flask(__name__)
CORS(app)

# Ana sayfa route'u
@app.route('/')
def home():
    return render_template('index.html')

# Dashboard route'u
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    output = None
    if request.method == 'POST':
        input_text = request.form.get('input_text')
        if input_text:
            output = get_response(input_text)
    return render_template('dashboard.html', output=output)

# Favicon için boş yanıt
@app.route('/favicon.ico')
def favicon():
    return '', 204

# Chat API route'u
@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("user_input")
        if not user_input:
            return jsonify({"error": "Mesaj boş olamaz"}), 400
        
        response = get_response(user_input)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": f"Sistem hatası: {str(e)}"}), 500

# Health check endpoint (Render için önemli)
@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "MindALT AI"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)