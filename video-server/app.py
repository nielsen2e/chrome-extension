import os
from flask import Flask, request, send_from_directory, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

CORS(app, resources={r"/*": {"origins": "*"}})

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request'}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method Not Allowed'}), 405

@app.errorhandler(413)
def payload_too_large(error):
    return jsonify({'error': 'Payload Too Large'}), 413

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    filename = request.headers.get('X-File-name')
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
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET'])
def index():
    videos = os.listdir(UPLOAD_FOLDER)
    return render_template_string('''
    <ul>
        {% for video in videos %}
        <li><a href="{{ url_for('uploaded_file', filename=video) }}">{{ video }}</a></li>
        {% endfor %}
    </ul>
    ''', videos=videos)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
