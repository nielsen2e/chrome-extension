import os
from flask import Flask, request, send_from_directory, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

# Enabling CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB

@app.route('/upload', methods=['POST'])
def upload_file():
    filename = request.headers.get('X-Filename')
    if not filename:
        return jsonify({'error': 'Missing filename header'}), 400

    content_length = request.content_length
    if content_length > app.config['MAX_CONTENT_LENGTH']:
        return jsonify({'error': 'File size exceeds the limit'}), 413

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    with open(file_path, 'wb') as f:
        f.write(request.get_data(cache=False))

    return jsonify({'success': 'File uploaded successfully'}), 200

@app.route('/videos/<filename>', methods=['GET'])
def uploaded_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

@app.route('/', methods=['GET'])
def index():
    try:
        videos = os.listdir(UPLOAD_FOLDER)
        return render_template_string('''
        <ul>
            {% for video in videos %}
            <li><a href="{{ url_for('uploaded_file', filename=video) }}">{{ video }}</a></li>
            {% endfor %}
        </ul>
        ''', videos=videos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
