import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-me')
    PORT = int(os.getenv('PORT', 3000))

    # Supabase
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
    SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')
    SUPABASE_BUCKET = os.getenv('SUPABASE_BUCKET', 'form-images')

    # Admin
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 24  # 1 day

    # Cache
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 60  # seconds
