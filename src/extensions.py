from flask_jwt_extended import JWTManager
from flask_caching import Cache
from supabase import create_client
from flask import current_app

jwt = JWTManager()
cache = Cache()

class SupabaseClientWrapper:
    def __init__(self):
        self.client = None

    def init_app(self, app):
        url = app.config.get('SUPABASE_URL')
        key = app.config.get('SUPABASE_SERVICE_ROLE_KEY')
        if not url or not key:
            app.logger.warning('Supabase config missing; supabase client will be unavailable')
            return
        self.client = create_client(url, key)

    def table(self, name):
        if not self.client:
            raise RuntimeError('Supabase client not initialized')
        return self.client.table(name)

supabase_client = SupabaseClientWrapper()
