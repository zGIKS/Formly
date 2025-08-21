from flask import Flask
from dotenv import load_dotenv
from .config import Config
from .extensions import jwt, cache, supabase_client

# blueprints
from .modules.auth.routes import auth_bp
from .modules.forms.routes import forms_bp
from .modules.questions.routes import questions_bp
from .modules.responses.routes import responses_bp
from .modules.storage.service import storage_bp
from .modules.health.routes import health_bp
from .modules.web.routes import web_bp


def create_app():
    load_dotenv()
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config())

    # init extensions
    jwt.init_app(app)
    cache.init_app(app)

    # supabase client stored in extension module
    supabase_client.init_app(app)

    # register blueprints
    app.register_blueprint(web_bp)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(forms_bp, url_prefix='/api/forms')
    app.register_blueprint(questions_bp, url_prefix='/api/questions')
    app.register_blueprint(responses_bp, url_prefix='/api/responses')
    app.register_blueprint(storage_bp, url_prefix='/api/storage')
    app.register_blueprint(health_bp, url_prefix='/api/health')

    return app
