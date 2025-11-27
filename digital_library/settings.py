"""
Django settings for digital_library project.
"""

from pathlib import Path
import os
# 🟢 IMPORTACIONES NECESARIAS PARA FIREBASE Y TESTS 🟢
import firebase_admin
from firebase_admin import credentials 
import sys # ⬅️ Importación para identificar modo de prueba

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-muibt=z5l8)b8__3a00&f)@@zg2h5aj^wk!n=2r5=)zdm-fi@_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # 💥 APLICACIONES NATIVAS (DEBEN IR PRIMERO) 💥
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Mis Apps (Pueden ir al final)
    'core',
    'libros',
]

# 💥 MIDDLEWARE CORREGIDO Y ORDENADO 💥
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Sesión debe ir antes de Auth
    'django.contrib.sessions.middleware.SessionMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', 
    'django.contrib.messages.middleware.MessageMiddleware', 
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'digital_library.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Ruta para templates globales (base.html)
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


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# ----------------------------------------------------
# 🚀 CONFIGURACIÓN DE RUTAS ABSOLUTAS (Firebase, Static, Media)
# ----------------------------------------------------

# Ruta absoluta para las credenciales de Firebase
FIREBASE_KEY_PATH = BASE_DIR / "firebase_key.json"

# Ruta para archivos estáticos (Necesario para producción/colectar)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Configuración de media (archivos subidos por el usuario)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ----------------------------------------------------
# 🧪 CONFIGURACIÓN PARA AMBIENTE DE PRUEBAS (TESTING) Y FIREBASE 
# ----------------------------------------------------

# Identifica si el comando 'test' está siendo ejecutado
TESTING = 'test' in sys.argv 

# Configuración de Firebase
FIREBASE_CONFIG = {
    'CREDENTIAL_FILE': FIREBASE_KEY_PATH,
    # 🛑 Deshabilita la sincronización si estamos en modo testing
    'SYNC_ENABLED': not TESTING,
}

# La lógica de inicialización se movería a un archivo de configuración de Firebase 
# o se llamaría on-demand, pero se remueve del settings.py

# ❌ Se ha quitado el bloque 'try...except' de inicialización directa de Firebase aquí.

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'