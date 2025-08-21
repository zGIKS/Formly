"""Check Supabase connectivity and list storage buckets.
Run: uv run python scripts/check_supabase.py
"""
import os
from dotenv import load_dotenv

load_dotenv()
import httpx

URL = os.getenv('SUPABASE_URL')
KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

if not URL or not KEY:
    print('SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY missing in .env')
    raise SystemExit(1)

endpoint = f"{URL.rstrip('/')}/storage/v1/buckets"
headers = {
    'apikey': KEY,
    'Authorization': f'Bearer {KEY}',
}

try:
    r = httpx.get(endpoint, headers=headers, timeout=10.0)
    if r.status_code != 200:
        print('Error listing buckets:', r.status_code, r.text)
        raise SystemExit(1)
    buckets = r.json()
    print('Buckets:')
    for b in buckets:
        print('-', b.get('name'))
    print('Storage URL:', endpoint)
except Exception as e:
    print('Error connecting to Supabase storage (HTTP):', e)
