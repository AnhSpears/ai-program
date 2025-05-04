from flask import Blueprint, request, jsonify, abort
from utils.auth import require_api_key
import subprocess, os

upgrade_bp = Blueprint('upgrade', __name__)

@upgrade_bp.route('/', methods=['POST'])
@require_api_key
def upgrade():
    data = request.json
    for path, content in data.get('files', {}).items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f: f.write(content)
    # git commit & push
    subprocess.run(['git','add','.'])
    subprocess.run(['git','commit','-m','AI upgrade'])
    subprocess.run(['git','push'])
    return jsonify({"status":"upgraded"})
