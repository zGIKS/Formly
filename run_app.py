#!/usr/bin/env python3
"""
Formly - Sistema de Gestión de Formularios
Ejecuta la aplicación Flask para desarrollo
"""

import os
import sys
from src.app import create_app

# Agregar el directorio raíz al path de Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    app = create_app()
    
    # Configuración para desarrollo
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 3000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print(f"""
    🚀 Formly - Sistema de Gestión de Formularios
    
    Servidor iniciado en: http://{host}:{port}
    
    📱 Rutas disponibles:
    • Panel Admin: http://{host}:{port}/admin/login
    • API Health: http://{host}:{port}/api/health
    
    💡 Para crear formularios, inicia sesión como admin con las credenciales del archivo .env
    """)
    
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    main()