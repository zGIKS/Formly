from flask import Blueprint, render_template, redirect, url_for

web_bp = Blueprint('web', __name__)

@web_bp.route('/')
def index():
    return redirect('/admin/login')

@web_bp.route('/admin')
def admin_index():
    return redirect('/admin/login')

@web_bp.route('/admin/login')
def admin_login():
    return render_template('login.html')

@web_bp.route('/admin/dashboard')
def admin_dashboard():
    return render_template('dashboard.html')

@web_bp.route('/admin/form/<form_id>/questions')
def admin_questions(form_id):
    return render_template('questions.html')

@web_bp.route('/admin/form/<slug>/edit')
def admin_edit_form(slug):
    return render_template('edit_form.html')

@web_bp.route('/form/<slug>')
def public_form(slug):
    return render_template('form.html')