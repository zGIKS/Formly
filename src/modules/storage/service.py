import uuid
from flask import Blueprint, current_app
from werkzeug.utils import secure_filename

storage_bp = Blueprint('storage', __name__)

from ...extensions import supabase_client
from flask_jwt_extended import jwt_required


@storage_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    # Uploads must be done by admin via backend (JWT guard enforced)
    from flask import request, jsonify
    f = request.files.get('file')
    if not f:
        return jsonify({'error': 'file required'}), 400

    filename = secure_filename(f.filename)
    key = str(uuid.uuid4()) + '_' + filename
    bucket = current_app.config.get('SUPABASE_BUCKET')
    sb = supabase_client.client.storage
    try:
        # supabase-py accepts file-like objects
        res = sb.from_(bucket).upload(key, f)
        public_url = sb.from_(bucket).get_public_url(key)
        return jsonify({'url': public_url, 'key': key}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@storage_bp.route('/delete', methods=['POST'])
@jwt_required()
def delete_file():
    from flask import request, jsonify
    key = request.json.get('key')
    if not key:
        return jsonify({'error': 'key required'}), 400
    bucket = current_app.config.get('SUPABASE_BUCKET')
    try:
        sb = supabase_client.client.storage
        sb.from_(bucket).remove([key])
        return jsonify({'deleted': key}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
