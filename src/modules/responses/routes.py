from flask import Blueprint, request, jsonify
from ...extensions import supabase_client

responses_bp = Blueprint('responses', __name__)


@responses_bp.route('/submit/<form_slug>', methods=['POST'])
def submit_response(form_slug):
    payload = request.get_json() or {}
    # expected: {'answers': [{'question_id':'...', 'selected': ['opt1','opt2'] or 'opt1' or 'text': '...'}], 'meta':{}}
    answers = payload.get('answers', [])

    # basic validation
    if not isinstance(answers, list) or not answers:
        return jsonify({'error': 'answers required'}), 400

    # fetch form
    form_res = supabase_client.table('forms').select('*').eq('slug', form_slug).maybe_single().execute()
    if not form_res or not form_res.data:
        return jsonify({'error': 'form not found'}), 404
    form = form_res.data

    # fetch questions
    qs_res = supabase_client.table('questions').select('*').eq('form_id', form['id']).execute()
    questions = {q['id']: q for q in (qs_res.data or [])}

    total_score = 0
    stored_answers = []
    for a in answers:
        q = questions.get(a.get('question_id'))
        if not q:
            return jsonify({'error': 'invalid question id', 'id': a.get('question_id')}), 400
        if q['type'] == 'TEXT':
            stored_answers.append({'question_id': q['id'], 'text': a.get('text')})
            continue
        # MULTIPLE_CHOICE expects single selected id
        if q['type'] == 'MULTIPLE_CHOICE':
            sel = a.get('selected')
            if not sel:
                return jsonify({'error': 'selection required for multiple choice', 'question': q['id']}), 400
            # find option
            opt = next((o for o in q.get('options', []) if o['id'] == sel), None)
            if not opt:
                return jsonify({'error': 'invalid option selected'}), 400
            total_score += int(opt.get('score', 0))
            stored_answers.append({'question_id': q['id'], 'selected': sel})
        elif q['type'] == 'CHECKBOXES':
            sels = a.get('selected') or []
            if not isinstance(sels, list):
                return jsonify({'error': 'selected must be list for checkboxes'}), 400
            for s in sels:
                opt = next((o for o in q.get('options', []) if o['id'] == s), None)
                if opt:
                    total_score += int(opt.get('score', 0))
            stored_answers.append({'question_id': q['id'], 'selected': sels})

    # determine interpretation
    interpretation = None
    for r in form.get('score_ranges', []):
        min_score = r.get('min', 0)
        max_score = r.get('max', 0)
        if total_score >= min_score and total_score <= max_score:
            interpretation = r.get('message')
            break

    record = {
        'id': None,
        'form_id': form['id'],
        'answers': stored_answers,
        'score': total_score,
        'interpretation': interpretation,
    }

    res = supabase_client.table('responses').insert(record).execute()
    return jsonify({'score': total_score, 'interpretation': interpretation}), 201
