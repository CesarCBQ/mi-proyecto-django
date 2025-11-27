"""
Django settings for digital_library project.
"""

from pathlib import Path
import os
import firebase_admin
from firebase_admin import credentials 
import dj_database_url

# --- RUTAS ---
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- CONFIGURACIÓN DE SEGURIDAD Y ENTORNO ---
# Usa una variable de entorno para la clave secreta, OBLIGATORIO en producción
SECRET_KEY = os.environ.get(
    'SECRET_KEY', 
    'django-insecure-muibt=z5l8)b8__3a00&f)@@zg2h5aj^wk!n=2r5=)zdm-fi@_' # Valor de desarrollo
)

# Controla DEBUG con una variable de entorno
DEBUG = os.environ.get('DEBUG') == 'True' 

# Permite cualquier host en Render
if not DEBUG:
    # URL de Render (si se despliega allí)
    ALLOWED_HOSTS = [os.environ.get('RENDER_EXTERNAL_HOSTNAME')]
else:
    # Permite acceso local
    ALLOWED_HOSTS = []


# --- DEFINICIÓN DE LA APLICACIÓN ---
INSTALLED_APPS = [
    # APLICACIONES NATIVAS 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Mis Apps
    'core',
    'libros',
]

# MIDDLEWARE: Asegúrate de incluir WhiteNoise si estás en producción
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', 
    'django.contrib.messages.middleware.MessageMiddleware', 
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 🟢 AGREGAR WHITENOISE AQUÍ (Necesario para servir archivos estáticos) 🟢
    'whitenoise.middleware.WhiteNoiseMiddleware', 
]

ROOT_URLCONF = 'digital_library.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Ruta para templates globales (base.html)
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'digital_library.wsgi.application'


# --- BASE DE DATOS ---
DATABASES = {
    'default': dj_database_url.config(
        # La variable de entorno DATABASE_URL es la que usará Render
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}

# Si no se encuentra 'DATABASE_URL', usa la configuración local (solo si DEBUG=True)
if DEBUG and not DATABASES['default']:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }


# --- VALIDACIÓN DE CONTRASEÑA, I18N Y ZONA HORARIA ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --- CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS (STATIC FILES) ---
STATIC_URL = '/static/'

# Configuración de media (archivos subidos por el usuario)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configuración exclusiva para producción (cuando DEBUG es False)
if not DEBUG:
    # Ruta donde WhiteNoise buscará archivos estáticos recolectados
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    
    # Almacenamiento optimizado de WhiteNoise para producción
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
else:
    # Asegura que STATIC_ROOT esté definido incluso en DEBUG para collectstatic
    STATIC_ROOT = BASE_DIR / 'staticfiles'


# --- FIREBASE ADMIN SDK ---

# Ruta absoluta para las credenciales de Firebase
# Opcionalmente, puedes usar una variable de entorno para el contenido del archivo
FIREBASE_KEY_PATH = BASE_DIR / "firebase_key.json"

try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(FIREBASE_KEY_PATH)
        firebase_admin.initialize_app(cred)
        print("Firebase Admin SDK inicializado.")
except FileNotFoundError:
    print(f"ADVERTENCIA: Archivo de credenciales de Firebase no encontrado en {FIREBASE_KEY_PATH}")
except Exception as e:
    # Maneja otros errores de inicialización o permisos
    print(f"ERROR al inicializar Firebase: {e}")