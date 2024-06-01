from flask import Flask, session, request, jsonify
from util import read_secret_key, save_user_file, delete_user_files, get_user_files, delete_user_file
import uuid

app = Flask(__name__)
app.secret_key = read_secret_key()

@app.before_request
def before_request():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())

@app.route("/logout")
def index():
    delete_user_files(session['user_id'])
    session.pop('user_id', None)
    return 'OK', 200

@app.route('/files', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part in the request.', 400
    
    file = request.files['file']
    
    if file.filename == '':
    
        return 'No file selected for uploading.', 400
    if file.content_type != 'application/pdf':
        return 'Uploaded file is not a PDF.', 400
    
    save_user_file(session['user_id'], file)

    return 'File successfully uploaded!', 200

@app.route('/files', methods=['GET'])
def get_files():
    user_files = get_user_files(session['user_id'])
    return jsonify(user_files)

@app.route('/files/<file_name>', methods=['DELETE'])
def delete_file(file_name: str):
    try:
        delete_user_file(session['user_id'], file_name)
        return "", 204
    except FileNotFoundError as e:
        return str(e), 400

@app.route("/health")
def index():
    return 'OK', 200

if __name__ == "__main__":
    app.run(debug=True)