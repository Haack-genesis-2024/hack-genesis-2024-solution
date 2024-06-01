from flask import Flask, session, request, jsonify
from files_service import save_file, get_files, delete_file
from secrets_service import read_secret
from conversations_service import delete_conversation, get_conversation
from ai_service import chat
import uuid
from flask_cors import CORS
from datetime import timedelta


app = Flask(__name__)

CORS(app, origins=["http://localhost:8080", "http://localhost:5173", "http://localhost:4173"], supports_credentials=True)

app.secret_key = read_secret('SESSION_KEY')
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(days=1)
app.config['SESSION_COOKIE_SAMESITE'] = 'None'

@app.before_request
def before_request():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
        session.permanent = True

@app.route("/logout")
def logout():
    delete_conversation(session.get('user_id'))
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
    
    save_file(file)

    return 'File successfully uploaded!', 200

@app.route('/files', methods=['GET'])
def get_files_handler():
    files = get_files()
    return jsonify(files)

@app.route('/files/<file_name>', methods=['DELETE'])
def delete_file_handler(file_name: str):
    try:
        delete_file(file_name)
        return "", 204
    except FileNotFoundError as e:
        return str(e), 400
  
@app.route('/chat', methods=['POST'])
def chat_handler():
    message = request.json.get('message')
    if message:
        try:
            messages = chat(session.get('user_id'), message)
            return jsonify(messages)
        except Exception as e:
            return str(e), 500
    else:
        return "No message provided", 400


@app.route('/chat', methods=['GET'])
def get_conversation_handler():
    return jsonify(get_conversation(session.get('user_id')))

@app.route("/health")
def index():
    return 'OK', 200

if __name__ == "__main__":
    app.run(debug=True)