from flask import Flask, request, jsonify, render_template, session, redirect, url_for, render_template_string
from flask_cors import CORS
import os
import sys
import sqlite3
from datetime import datetime
from functools import wraps

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from mindalt_ai import get_response
    print("✓ mindalt_ai modülü başarıyla yüklendi!")
except ImportError as e:
    print(f"✗ mindalt_ai import hatası: {e}")
    import importlib.util
    spec = importlib.util.spec_from_file_location("mindalt_ai", "mindalt_ai.py")
    mindalt_ai = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mindalt_ai)
    get_response = mindalt_ai.get_response

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "mindalt-super-secret-key-2025")

CORS(app, resources={r"/*": {"origins": ["https://mindaltai.com", "https://www.mindaltai.com", "http://localhost:*", "http://127.0.0.1:*"]}})

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "mindalt2025")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def init_db():
    conn = sqlite3.connect('mindalt_stats.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS visits (id INTEGER PRIMARY KEY AUTOINCREMENT, ip_address TEXT NOT NULL, visit_date TEXT NOT NULL, UNIQUE(ip_address, visit_date))')
    c.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, ip_address TEXT NOT NULL, message_date TEXT NOT NULL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    conn.close()

init_db()

def log_visit(ip_address):
    today = datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect('mindalt_stats.db')
    c = conn.cursor()
    try:
        c.execute('INSERT OR IGNORE INTO visits (ip_address, visit_date) VALUES (?, ?)', (ip_address, today))
        conn.commit()
    except:
        pass
    conn.close()

def log_message(ip_address):
    today = datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect('mindalt_stats.db')
    c = conn.cursor()
    c.execute('INSERT INTO messages (ip_address, message_date) VALUES (?, ?)', (ip_address, today))
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect('mindalt_stats.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(DISTINCT ip_address) FROM visits')
    total_users = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM messages')
    total_messages = c.fetchone()[0]
    today = datetime.now().strftime('%Y-%m-%d')
    c.execute('SELECT COUNT(DISTINCT ip_address) FROM visits WHERE visit_date = ?', (today,))
    today_users = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM messages WHERE message_date = ?', (today,))
    today_messages = c.fetchone()[0]
    conn.close()
    return {'total_users': total_users, 'total_messages': total_messages, 'today_users': today_users, 'today_messages': today_messages}

@app.route('/')
def home():
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip_address:
        ip_address = ip_address.split(',')[0].strip()
    log_visit(ip_address)
    return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    output = None
    if request.method == 'POST':
        input_text = request.form.get('input_text')
        if input_text:
            output = get_response(input_text)
    return render_template('dashboard.html', output=output)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            return render_template_string('<h1>Hatalı şifre!</h1><a href="/admin/login">Tekrar dene</a>')
    return render_template_string('<html><body><h1>Admin Girişi</h1><form method="POST"><input type="password" name="password" required><button>Giriş</button></form></body></html>')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/stats')
@login_required
def admin_stats():
    stats = get_stats()
    return jsonify(stats)

@app.route('/admin')
@login_required
def admin_panel():
    return render_template_string('<html><body><h1>Admin Panel</h1><div id="stats"></div><button onclick="location.reload()">Yenile</button><button onclick="location.href=\'/admin/logout\'">Çıkış</button><script>fetch("/admin/stats").then(r=>r.json()).then(d=>{document.getElementById("stats").innerHTML=`<p>Toplam: ${d.total_users} kullanıcı, ${d.total_messages} mesaj</p><p>Bugün: ${d.today_users} kullanıcı, ${d.today_messages} mesaj</p>`})</script></body></html>')

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("user_input")
        if not user_input:
            return jsonify({"error": "Mesaj boş olamaz"}), 400
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
        if ip_address:
            ip_address = ip_address.split(',')[0].strip()
        log_message(ip_address)
        response = get_response(user_input)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": f"Sistem hatası: {str(e)}"}), 500

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "MindALT AI"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)