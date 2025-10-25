from flask import Flask, render_template, request, jsonify
from mindalt_ai import get_response

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    output = None
    if request.method == 'POST':
        input_text = request.form.get('input_text')
        if input_text:
            output = get_response(input_text)
    return render_template('dashboard.html', output=output)

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        question = data.get('question', '')
        if not question:
            return jsonify({'error': 'Soru boş olamaz.'})
        answer = get_response(question)
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
