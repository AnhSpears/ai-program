import os, sys, time, subprocess, threading
from flask import Flask, request, jsonify, abort, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_session import Session
import redis
import openai
import config
from embedder import add_document, query_similar

# App
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
app.config['UPLOAD_FOLDER']   = config.UPLOAD_FOLDER

# Session Redis
app.config.update({
    'SESSION_TYPE': 'redis',
    'SESSION_REDIS': redis.from_url(config.REDIS_URL),
    'SESSION_PERMANENT': False
})
Session(app)
# Rate limiter
limiter = Limiter(app, key_func=get_remote_address, default_limits=[config.RATE_LIMIT])
# OpenAI
openai.api_key = config.OPENAI_API_KEY

# Chat endpoint
@app.route('/chat', methods=['POST'])
@limiter.limit(config.RATE_LIMIT)
def chat():
    data = request.get_json() or {}
    msg  = data.get('message','').strip()
    if not msg:
        return abort(400)
    history = request.session.get('history', [])
    # Kéo ngữ cảnh từ vector store
    docs = query_similar(msg)
    system = [{'role':'system','content':'Bạn là AI trợ lý.'}]
    # Ghép thêm tài liệu liên quan
    for doc in docs:
        system.append({'role':'system','content':f'Context: {doc}'})
    conv = system + history + [{'role':'user','content':msg}]
    resp = openai.ChatCompletion.create(model='gpt-4o-mini', messages=conv)
    ai_msg = resp.choices[0].message.content
    history.extend([{'role':'user','content':msg},{'role':'assistant','content':ai_msg}])
    request.session['history'] = history
    return jsonify({'response': ai_msg})

# File upload
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return abort(400)
    f = request.files['file']
    path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
    f.save(path)
    # Đọc nội dung (TXT, PDF, DOCX)...
    import textract
    text = textract.process(path).decode('utf-8', errors='ignore')
    add_document(f.filename, text)
    return jsonify({'status':'uploaded','file':f.filename})

# Static serve uploads
@app.route('/uploads/<filename>')
def serve_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Admin upgrade (giữ nguyên)
@app.route('/upgrade', methods=['POST'])
def upgrade(): ...  # như trước

# Git watcher thread
def watcher(): ...

if __name__ == '__main__':
    # Tạo uploads dir
    os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
    th = threading.Thread(target=watcher, daemon=True)
    th.start()
    app.run(host='0.0.0.0', port=5000)
