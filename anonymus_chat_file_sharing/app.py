from flask import Flask, render_template, request, send_from_directory, jsonify, session
from datetime import datetime
import os
import uuid

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'uploads'
chat_history = []

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.before_request
def assign_user():
    if 'user_id' not in session:
        session['user_id'] = f"User{str(uuid.uuid4())[:5]}"
        time = datetime.now().strftime("%H:%M:%S")
        join_message = f"🔔 {session['user_id']} joined the chat"
        chat_history.append({"message": join_message, "time": time})

@app.route('/')
def index():
    return render_template('index.html', user_id=session['user_id'])

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form.get('message')
    user_id = session['user_id']
    time = datetime.now().strftime("%H:%M:%S")
    if message:
        chat_history.append({"message": f"<b>{user_id}</b>: {message}", "time": time})
    return '', 204

@app.route('/get_messages')
def get_messages():
    return jsonify(chat_history)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    user_id = session['user_id']
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    time = datetime.now().strftime("%H:%M:%S")
    chat_history.append({
        "message": f"📁 <b>{user_id}</b> shared a file: <a href='/download/{filename}' target='_blank'>{filename}</a>",
        "time": time
    })
    return '', 204

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/user_left', methods=['POST'])
def user_left():
    user_id = session.get('user_id')
    if user_id:
        time = datetime.now().strftime("%H:%M:%S")
        leave_message = f"🔕 {user_id} left the chat"
        chat_history.append({"message": leave_message, "time": time})
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
