import uuid
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .dto import QuestionCreateDTO
from ...extensions import supabase_client

questions_bp = Blueprint('questions', __name__)


@questions_bp.route('/', methods=['POST'])
@jwt_required()
def create_question():
    data = request.get_json() or {}
    try:
        dto = QuestionCreateDTO(**data)
    except Exception as e:
        return jsonify({'error': 'invalid payload', 'detail': str(e)}), 400

    if dto.type not in ('MULTIPLE_CHOICE', 'CHECKBOXES', 'TEXT'):
        return jsonify({'error': 'unsupported question type'}), 400

    q = {
        'id': str(uuid.uuid4()),
        'form_id': dto.form_id,
        'text': dto.text,
        'type': dto.type,
        'image': dto.image,
        'options': [o.dict() for o in dto.options] if dto.options else []
    }

    res = supabase_client.table('questions').insert(q).execute()
    return jsonify({'question': q, 'res': getattr(res, 'data', None)}), 201


@questions_bp.route('/by_form/<form_id>', methods=['GET'])
def list_by_form(form_id):
    res = supabase_client.table('questions').select('*').eq('form_id', form_id).execute()
    return jsonify(res.data or []), 200


@questions_bp.route('/<question_id>', methods=['DELETE'])
@jwt_required()
def delete_question(question_id):
    res = supabase_client.table('questions').delete().eq('id', question_id).execute()
    return jsonify({'deleted': question_id}), 200


@questions_bp.route('/<question_id>', methods=['PUT'])
@jwt_required()
def update_question(question_id):
    data = request.get_json() or {}
    try:
        dto = QuestionCreateDTO(**data)
    except Exception as e:
        return jsonify({'error': 'invalid payload', 'detail': str(e)}), 400

    if dto.type not in ('MULTIPLE_CHOICE', 'CHECKBOXES', 'TEXT'):
        return jsonify({'error': 'unsupported question type'}), 400

    updates = {
        'text': dto.text,
        'type': dto.type,
        'image': dto.image,
        'options': [o.dict() for o in dto.options] if dto.options else []
    }

    res = supabase_client.table('questions').update(updates).eq('id', question_id).execute()
    return jsonify({'question': updates, 'res': getattr(res, 'data', None)}), 200
