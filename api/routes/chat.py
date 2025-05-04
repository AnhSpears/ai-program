from flask import Blueprint, request, jsonify
import openai
from config import OPENAI_API_KEY
from models.vector_store import retrieve_context

openai.api_key = OPENAI_API_KEY
chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt', '')
    # RAG: lấy context
    context = retrieve_context(prompt)
    messages = [{"role":"system","content":context}, {"role":"user","content":prompt}]
    resp = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    return jsonify(resp.choices[0].message)
