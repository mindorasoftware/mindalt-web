<!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Admin Girişi</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                    height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0;
                }
                .login-box {
                    background: white;
                    padding: 40px;
                    border-radius: 16px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    text-align: center;
                }
                h1 {
                    color: #1e3c72;
                    margin-bottom: 20px;
                }
                input {
                    width: 100%;
                    padding: 12px;
                    margin: 10px 0;
                    border: 2px solid #ddd;
                    border-radius: 8px;
                    font-size: 16px;
                }
                button {
                    width: 100%;
                    padding: 14px;
                    background: linear-gradient(135deg, #2a5298, #1e3c72);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: 600;
                    cursor: pointer;
                    margin-top: 10px;
                }
                button:hover {
                    opacity: 0.9;
                }
            </style>
        </head>
        <body>
            <div class="login-box">
                <h1>🔒 Admin Girişi</h1>
                <form method="GET" action="/admin">
                    <input type="text" name="username" placeholder="Kullanıcı Adı" value="admin" readonly>
                    <input type="password" name="password" placeholder="Şifre" id="password" required>
                    <button type="button" onclick="login()">Giriş Yap</button>
                </form>
            </div>
            <script>
                function login() {
                    const password = document.getElementById('password').value;
                    if (!password) {
                        alert('Lütfen şifrenizi girin!');
                        return;
                    }
                    // Basic Auth ile sayfa yenile
                    const url = '/admin';
                    fetch(url, {
                        method: 'GET',
                        headers: {
                            'Authorization': 'Basic ' + btoa('admin:' + password)
                        }
                    }).then(response => {
                        if (response.ok) {
                            // Şifre doğru, sayfayı yenile
                            window.location.href = url + '?auth=' + btoa('admin:' + password);
                        } else {
                            alert('Hatalı şifre!');
                        }
                    }).catch(err => {
                        alert('Bağlantı hatası!');
                    });
                }
            </script>
        </body>
        </html>
        ''', 401, {'WWW-Authenticate': 'Basic realm="Admin Login"'}from flask import Flask, request, jsonify, render_template, session, redirect, url_for, render_template_string
from flask_cors import CORS
import os
import sys
import sqlite3
from datetime import datetime
from functools import wraps

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
app.secret_key = os.environ.get("SECRET_KEY", "mindalt-super-secret-key-2025")

# CORS ayarları - sadece kendi domain'inden isteklere izin ver
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://mindaltai.com",
            "https://www.mindaltai.com",
            "http://localhost:*",
            "http://127.0.0.1:*"
        ]
    }
})

# Admin şifresi (ortam değişkeninden al veya varsayılan kullan)
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "mindalt2025")

# SQLite Veritabanı Kurulumu
def init_db():
    conn = sqlite3.connect('mindalt_stats.db')
    c = conn.cursor()
    
    # Kullanıcı ziyaretleri tablosu
    c.execute('''
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT NOT NULL,
            visit_date TEXT NOT NULL,
            UNIQUE(ip_address, visit_date)
        )
    ''')
    
    # Mesaj sayacı tablosu
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT NOT NULL,
            message_date TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Veritabanını başlat
init_db()

# Kullanıcı ziyaretini kaydet
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

# Mesaj sayısını artır
def log_message(ip_address):
    today = datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect('mindalt_stats.db')
    c = conn.cursor()
    c.execute('INSERT INTO messages (ip_address, message_date) VALUES (?, ?)', (ip_address, today))
    conn.commit()
    conn.close()

# İstatistikleri getir
def get_stats():
    conn = sqlite3.connect('mindalt_stats.db')
    c = conn.cursor()
    
    # Toplam tekil kullanıcı sayısı
    c.execute('SELECT COUNT(DISTINCT ip_address) FROM visits')
    total_users = c.fetchone()[0]
    
    # Toplam mesaj sayısı
    c.execute('SELECT COUNT(*) FROM messages')
    total_messages = c.fetchone()[0]
    
    # Bugünkü kullanıcı sayısı
    today = datetime.now().strftime('%Y-%m-%d')
    c.execute('SELECT COUNT(DISTINCT ip_address) FROM visits WHERE visit_date = ?', (today,))
    today_users = c.fetchone()[0]
    
    # Bugünkü mesaj sayısı
    c.execute('SELECT COUNT(*) FROM messages WHERE message_date = ?', (today,))
    today_messages = c.fetchone()[0]
    
    conn.close()
    
    return {
        'total_users': total_users,
        'total_messages': total_messages,
        'today_users': today_users,
        'today_messages': today_messages
    }

# Ana sayfa route'u
@app.route('/')
def home():
    # Kullanıcı IP'sini al
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip_address:
        ip_address = ip_address.split(',')[0].strip()
    log_visit(ip_address)
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

# Admin Login Sayfası
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            return render_template_string(LOGIN_TEMPLATE, error="Hatalı şifre!")
    return render_template_string(LOGIN_TEMPLATE)

# Admin Logout
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

# Login Template
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Girişi - MindALT AI</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-box {
            background: white;
            padding: 50px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
            text-align: center;
            width: 400px;
        }
        h1 {
            font-size: 28px;
            background: linear-gradient(135deg, #2a5298, #1e3c72);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 30px;
        }
        input[type="password"] {
            width: 100%;
            padding: 15px;
            margin: 15px 0;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s;
        }
        input[type="password"]:focus {
            outline: none;
            border-color: #2a5298;
        }
        button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #2a5298, #1e3c72);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            margin-top: 10px;
            transition: all 0.3s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(42, 82, 152, 0.4);
        }
        .error {
            color: #e74c3c;
            margin-top: 15px;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <h1>🔒 Admin Girişi</h1>
        <form method="POST">
            <input type="password" name="password" placeholder="Admin Şifresi" required autofocus>
            <button type="submit">Giriş Yap</button>
            {% if error %}
            <div class="error">{{ error }}</div>
            {% endif %}
        </form>
    </div>
</body>
</html>
'''

# Admin İstatistik API
@app.route('/admin/stats')
@login_required
def admin_stats():
    stats = get_stats()
    return jsonify(stats)

# Admin Panel
@app.route('/admin')
@login_required
def admin_panel():
    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Admin Girişi</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                    height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0;
                }
                .login-box {
                    background: white;
                    padding: 40px;
                    border-radius: 16px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    text-align: center;
                }
                h1 {
                    color: #1e3c72;
                    margin-bottom: 20px;
                }
                input {
                    width: 100%;
                    padding: 12px;
                    margin: 10px 0;
                    border: 2px solid #ddd;
                    border-radius: 8px;
                    font-size: 16px;
                }
                button {
                    width: 100%;
                    padding: 14px;
                    background: linear-gradient(135deg, #2a5298, #1e3c72);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: 600;
                    cursor: pointer;
                    margin-top: 10px;
                }
                button:hover {
                    opacity: 0.9;
                }
            </style>
        </head>
        <body>
            <div class="login-box">
                <h1>🔒 Admin Girişi</h1>
                <form method="GET" action="/admin">
                    <input type="text" name="username" placeholder="Kullanıcı Adı" value="admin" readonly>
                    <input type="password" name="password" placeholder="Şifre" id="password" required>
                    <button type="button" onclick="login()">Giriş Yap</button>
                </form>
            </div>
            <script>
                function login() {
                    const password = document.getElementById('password').value;
                    if (!password) {
                        alert('Lütfen şifrenizi girin!');
                        return;
                    }
                    // Basic Auth ile sayfa yenile
                    const url = '/admin';
                    fetch(url, {
                        method: 'GET',
                        headers: {
                            'Authorization': 'Basic ' + btoa('admin:' + password)
                        }
                    }).then(response => {
                        if (response.ok) {
                            // Şifre doğru, sayfayı yenile
                            window.location.href = url + '?auth=' + btoa('admin:' + password);
                        } else {
                            alert('Hatalı şifre!');
                        }
                    }).catch(err => {
                        alert('Bağlantı hatası!');
                    });
                }
            </script>
        </body>
        </html>
        ''', 401, {'WWW-Authenticate': 'Basic realm="Admin Login"'}
    
    return '''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MindALT AI - Admin Panel</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e8ba3 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 24px;
                padding: 40px;
                max-width: 800px;
                width: 100%;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            }
            h1 {
                font-size: 32px;
                background: linear-gradient(135deg, #2a5298, #1e3c72);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 30px;
                text-align: center;
            }
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .stat-card {
                background: linear-gradient(135deg, #2a5298, #1e3c72);
                color: white;
                padding: 30px;
                border-radius: 16px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(42, 82, 152, 0.3);
            }
            .stat-number {
                font-size: 48px;
                font-weight: 700;
                margin-bottom: 10px;
            }
            .stat-label {
                font-size: 16px;
                opacity: 0.9;
            }
            .refresh-btn {
                width: 100%;
                padding: 16px;
                background: linear-gradient(135deg, #2a5298, #1e3c72);
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s;
            }
            .refresh-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(42, 82, 152, 0.4);
            }
            .last-update {
                text-align: center;
                color: #666;
                margin-top: 20px;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 MindALT AI İstatistikleri</h1>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number" id="totalUsers">-</div>
                    <div class="stat-label">Toplam Kullanıcı</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-number" id="totalMessages">-</div>
                    <div class="stat-label">Toplam Mesaj</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-number" id="todayUsers">-</div>
                    <div class="stat-label">Bugünkü Kullanıcı</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-number" id="todayMessages">-</div>
                    <div class="stat-label">Bugünkü Mesaj</div>
                </div>
            </div>
            
            <button class="refresh-btn" onclick="loadStats()">🔄 Yenile</button>
            <button class="refresh-btn" onclick="logout()" style="background: #e74c3c; margin-top: 10px;">🚪 Çıkış Yap</button>
            
            <div class="last-update" id="lastUpdate">-</div>
        </div>

        <script>
            async function loadStats() {
                try {
                    const response = await fetch('/admin/stats');
                    
                    if (!response.ok) {
                        window.location.href = '/admin/login';
                        return;
                    }
                    
                    const data = await response.json();
                    
                    document.getElementById('totalUsers').textContent = data.total_users;
                    document.getElementById('totalMessages').textContent = data.total_messages;
                    document.getElementById('todayUsers').textContent = data.today_users;
                    document.getElementById('todayMessages').textContent = data.today_messages;
                    
                    const now = new Date().toLocaleString('tr-TR');
                    document.getElementById('lastUpdate').textContent = 'Son güncelleme: ' + now;
                } catch (error) {
                    alert('İstatistikler yüklenemedi: ' + error.message);
                }
            }
            
            function logout() {
                window.location.href = '/admin/logout';
            }
            
            // Sayfa yüklenince istatistikleri getir
            loadStats();
            
            // Her 30 saniyede bir otomatik yenile
            setInterval(loadStats, 30000);
        </script>
    </body>
    </html>
    '''

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
        
        # Kullanıcı IP'sini al ve mesajı kaydet
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
        if ip_address:
            ip_address = ip_address.split(',')[0].strip()
        log_message(ip_address)
        
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