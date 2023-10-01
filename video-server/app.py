import os
from flask import Flask, request, send_from_directory, render_template_string
from flask_cors import CORS


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

#Enabling CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return 'File uploaded successfully', 200

@app.route('/videos/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/')
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
    app.run(debug=True)
