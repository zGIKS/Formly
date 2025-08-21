from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .dto import LoginDTO

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    try:
        dto = LoginDTO(**data)
    except Exception as e:
        return jsonify({'error': 'invalid payload', 'detail': str(e)}), 400

    admin_email = current_app.config.get('ADMIN_EMAIL')
    admin_password = current_app.config.get('ADMIN_PASSWORD')

    if dto.email != admin_email or dto.password != admin_password:
        return jsonify({'error': 'invalid credentials'}), 401

    token = create_access_token(identity={'email': dto.email})
    return jsonify({'access_token': token}), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    identity = get_jwt_identity()
    return jsonify({'admin': identity}), 200
