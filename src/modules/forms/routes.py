import uuid
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from .dto import FormCreateDTO
from ...extensions import supabase_client, cache

forms_bp = Blueprint('forms', __name__)


@forms_bp.route('/', methods=['POST'])
@jwt_required()
def create_form():
    data = request.get_json() or {}
    try:
        dto = FormCreateDTO(**data)
    except Exception as e:
        return jsonify({'error': 'invalid payload', 'detail': str(e)}), 400

    # limit to 3 forms
    table = supabase_client.table('forms')
    existing = table.select('id').execute()
    if existing and existing.data and len(existing.data) >= 3:
        return jsonify({'error': 'form limit reached (3)'}), 400

    new = {
        'id': str(uuid.uuid4()),
        'title': dto.title,
        'description': dto.description,
        'font_family': dto.font_family,
        'background_image': dto.background_image,
        'slug': dto.slug or (dto.title.lower().replace(' ', '-') + '-' + str(uuid.uuid4())[:8]),
        'score_ranges': dto.score_ranges or []
    }

    res = table.insert(new).execute()
    return jsonify({'form': new, 'res': getattr(res, 'data', None)}), 201


@forms_bp.route('/<slug>', methods=['GET'])
def get_form(slug):
    # cached public read
    cache_key = f'form:{slug}'
    cached = cache.get(cache_key)
    if cached:
        return jsonify(cached), 200

    table = supabase_client.table('forms')
    res = table.select('*').eq('slug', slug).maybe_single().execute()
    if not res or not res.data:
        return jsonify({'error': 'not found'}), 404
    cache.set(cache_key, res.data, timeout=60)
    return jsonify(res.data), 200


@forms_bp.route('/', methods=['GET'])
@jwt_required()
def list_forms_admin():
    """List all forms (admin view)."""
    table = supabase_client.table('forms')
    res = table.select('*').execute()
    return jsonify(res.data or []), 200


@forms_bp.route('/<slug>', methods=['PUT'])
@jwt_required()
def update_form(slug):
    data = request.get_json() or {}
    try:
        dto = FormCreateDTO(**data)
    except Exception as e:
        return jsonify({'error': 'invalid payload', 'detail': str(e)}), 400

    updates = {
        'title': dto.title,
        'description': dto.description,
        'font_family': dto.font_family,
        'background_image': dto.background_image,
        'score_ranges': dto.score_ranges or []
    }

    table = supabase_client.table('forms')
    res = table.update(updates).eq('slug', slug).execute()
    return jsonify({'form': updates, 'res': getattr(res, 'data', None)}), 200


@forms_bp.route('/<slug>', methods=['DELETE'])
@jwt_required()
def delete_form(slug):
    table = supabase_client.table('forms')
    res = table.delete().eq('slug', slug).execute()
    return jsonify({'deleted': slug}), 200
