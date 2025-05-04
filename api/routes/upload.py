from flask import Blueprint, request, jsonify
from services.extractor import extract_text
from services.embedding import embed_and_store
from config import BLOB_CONN_STR

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/', methods=['POST'])
def upload():
    file = request.files['file']
    # 1. Đưa lên Blob (bỏ code chi tiết)
    blob_url = upload_to_blob(file, BLOB_CONN_STR)
    text = extract_text(blob_url)
    embed_and_store(text)
    return jsonify({"status":"ok","url":blob_url})
