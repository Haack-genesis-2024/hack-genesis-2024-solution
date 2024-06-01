from flask import Flask, session, request, jsonify
from files_service import save_file, get_files, delete_file
from secrets_service import read_secret
from conversations_service import delete_conversation
from ai_service import chat
import uuid


app = Flask(__name__)
app.secret_key = read_secret('SESSION_KEY')

@app.before_request
def before_request():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())

@app.route("/logout")
def logout():
    delete_conversation(session['user_id'])
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
def get_files():
    files = get_files()
    return jsonify(files)

@app.route('/files/<file_name>', methods=['DELETE'])
def delete_file(file_name: str):
    try:
        delete_file(file_name)
        return "", 204
    except FileNotFoundError as e:
        return str(e), 400
  
@app.route('/chat', methods=['POST'])
def chat_with_ai():
    message = request.json.get('message')
  
    if message:
        try:
            response_message = chat(session['user_id'], message)
            return response_message, 200
        except Exception as e:
            return str(e), 500
    else:
        return "No message provided", 400


@app.route("/health")
def index():
    return 'OK', 200

if __name__ == "__main__":
    app.run(debug=True)