# 📝 FORMLY - Sistema de Gestión de Formularios

**Formly** es un sistema completo de gestión de formularios construido con Flask y Supabase. Permite a administradores crear formularios personalizables con sistema de puntuación y obtener respuestas de usuarios con resultados automáticos.

## ✨ Características

- **🔐 Autenticación de Administrador**: Login seguro con JWT
- **📋 Creación de Formularios**: Interface intuitiva tipo Google Forms
- **🎯 Tipos de Preguntas**: 
  - Opción múltiple
  - Casillas de verificación
  - Texto libre
- **📊 Sistema de Puntuación**: Configuración de rangos y mensajes personalizados
- **🎨 Personalización**: 
  - Tipografías personalizables
  - Imágenes de fondo
  - Imágenes en preguntas y opciones
- **🔗 Enlaces Compartibles**: URLs únicas para cada formulario
- **📱 Responsive**: Diseño adaptable a dispositivos móviles
- **☁️ Almacenamiento**: Integrado con Supabase Storage

## 🛠️ Instalación

### Prerrequisitos

- Python 3.8+
- Cuenta de Supabase
- Base de datos PostgreSQL (Supabase)

### 1. Configurar Variables de Entorno

Las credenciales ya están configuradas en el archivo `.env`. Puedes cambiar las credenciales de administrador si lo deseas:

```bash
# Administrador
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=change-me
```

### 2. Instalar Dependencias

**Opción A: Usando uv (Recomendado)**

```bash
# Instalar uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Crear entorno virtual y instalar dependencias
uv venv
uv pip sync requirements.txt
source .venv/bin/activate
```

**Opción B: Usando pip tradicional**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Inicializar Base de Datos

```bash
python scripts/init_db.py
```

### 4. Ejecutar la Aplicación

```bash
python run_app.py
```

O usando Flask:

```bash
FLASK_APP=run.py FLASK_ENV=development flask run --port=3000
```

Para producción con uvicorn:

```bash
uvicorn src.asgi:app --host 0.0.0.0 --port 3000 --reload
```

La aplicación estará disponible en `http://localhost:3000`

## 🚀 Uso

### Para Administradores

1. **Accede al Panel**: `http://localhost:3000/admin/login`
2. **Inicia Sesión**: Usa las credenciales configuradas en `.env`
3. **Crea Formularios**: 
   - Título y descripción
   - Configuración de rangos de puntuación
   - Personalización visual
4. **Agrega Preguntas**: Define preguntas con opciones y puntuaciones
5. **Comparte**: Copia el enlace único del formulario

### Para Usuarios

1. **Accede al Formulario**: Usa el enlace compartido (`/form/{slug}`)
2. **Completa las Respuestas**: Responde todas las preguntas
3. **Obtén Resultados**: Ve tu puntuación e interpretación automática

## 📁 Estructura del Proyecto

```
FORMLY/
├── src/
│   ├── app.py              # Aplicación principal Flask
│   ├── config.py           # Configuración
│   ├── extensions.py       # Extensiones (JWT, Cache, Supabase)
│   ├── templates/          # Plantillas HTML
│   └── modules/
│       ├── auth/           # Autenticación
│       ├── forms/          # Gestión de formularios
│       ├── questions/      # Gestión de preguntas
│       ├── responses/      # Respuestas de usuarios
│       ├── storage/        # Almacenamiento de archivos
│       └── web/            # Rutas web
├── scripts/
│   ├── init_db.py          # Inicialización de BD
│   └── check_supabase.py   # Verificación de conexión
├── requirements.txt        # Dependencias Python
├── run_app.py             # Script de ejecución
└── .env                   # Variables de entorno
```

## 🎯 Ejemplo de Uso: Formulario de Bullying

1. **Crear Formulario**:
   - Título: "Evaluación de Bullying Escolar"
   - Descripción: "Ayúdanos a entender tu experiencia"

2. **Configurar Rangos de Puntuación**:
   - 0-3 puntos: "No hay indicios de bullying"
   - 4-7 puntos: "Posibles situaciones de bullying"
   - 8-10 puntos: "Indicios claros de bullying"

3. **Agregar Preguntas**:
   - "¿Te insultan frecuentemente?" (Opción múltiple: Sí=5pts, No=0pts)
   - "¿Qué situaciones has vivido?" (Checkboxes: Empujones=2pts, Exclusión=3pts)
   - "Describe una experiencia" (Texto libre)

4. **Resultado**: El usuario obtiene una puntuación automática y mensaje correspondiente

## 🔧 Funcionalidades Implementadas

### Módulos Incluidos
- **auth**: Autenticación de administrador con JWT
- **forms**: Gestión completa de formularios
- **questions**: Creación y edición de preguntas
- **responses**: Procesamiento de respuestas y puntuación
- **storage**: Integración con Supabase Storage
- **web**: Interface web completa
- **health**: Endpoint de salud para monitoreo

### Interface Web
- Panel de administración completo
- Formularios públicos responsivos
- Gestión de preguntas con editor visual
- Sistema de puntuación en tiempo real

## 🔒 Seguridad

- Autenticación JWT para administradores
- Validación de datos con Pydantic
- Sanitización de archivos subidos
- Variables de entorno para credenciales
- Límite de 3 formularios por admin

## 📝 Notas de Desarrollo

- Archivos mantenidos pequeños y modulares (200-300 LOC máx.)
- Código limpio y bien estructurado
- Diseño inspirado en Google Forms
- Totalmente funcional out-of-the-box

---

**Desarrollado con ❤️ usando Flask y Supabase**
