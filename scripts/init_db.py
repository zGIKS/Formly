"""Initialize Supabase/Postgres tables required for the app.
This script uses SUPABASE_DB_URL to connect directly to PostgreSQL.
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv('SUPABASE_DB_URL')

if not DB_URL:
    print('Set SUPABASE_DB_URL in .env file')
    raise SystemExit(1)

# SQL para crear las tablas
sql_commands = [
    '''
    CREATE TABLE IF NOT EXISTS forms (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        title TEXT NOT NULL,
        description TEXT,
        font_family TEXT DEFAULT 'Inter',
        background_image TEXT,
        slug TEXT UNIQUE NOT NULL,
        score_ranges JSONB DEFAULT '[]'::jsonb,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS questions (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        form_id UUID NOT NULL REFERENCES forms(id) ON DELETE CASCADE,
        text TEXT NOT NULL,
        type TEXT NOT NULL CHECK (type IN ('MULTIPLE_CHOICE', 'CHECKBOXES', 'TEXT')),
        image TEXT,
        options JSONB DEFAULT '[]'::jsonb,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS responses (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        form_id UUID NOT NULL REFERENCES forms(id) ON DELETE CASCADE,
        answers JSONB NOT NULL,
        score INTEGER DEFAULT 0,
        interpretation TEXT,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    ''',
    '''
    CREATE INDEX IF NOT EXISTS idx_forms_slug ON forms(slug);
    ''',
    '''
    CREATE INDEX IF NOT EXISTS idx_questions_form_id ON questions(form_id);
    ''',
    '''
    CREATE INDEX IF NOT EXISTS idx_responses_form_id ON responses(form_id);
    '''
]

try:
    print('🔄 Conectando a la base de datos...')
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()
    
    print('🔄 Creando tablas...')
    
    for i, sql in enumerate(sql_commands, 1):
        print(f'   Ejecutando comando {i}/{len(sql_commands)}...')
        cursor.execute(sql)
    
    conn.commit()
    
    # Verificar que las tablas se crearon
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name IN ('forms', 'questions', 'responses')
        ORDER BY table_name;
    """)
    
    tables = cursor.fetchall()
    
    print('✅ Tablas creadas exitosamente:')
    for table in tables:
        print(f'   • {table[0]}')
    
    cursor.close()
    conn.close()
    
    print('\n🎉 Base de datos inicializada correctamente!')
    print('\n📝 Ahora puedes ejecutar: python run_app.py')

except psycopg2.Error as e:
    print(f'❌ Error de PostgreSQL: {e}')
    raise SystemExit(1)
except Exception as e:
    print(f'❌ Error: {e}')
    raise SystemExit(1)
