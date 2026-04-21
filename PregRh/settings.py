from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Media
MEDIA_URL = '/banco/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Seguridad
SECRET_KEY = 'django-insecure-pk5o*^zd1+v(5=!us^pbch6+m4rd_7=mggueb^+1^$e!)1d8hx'
DEBUG = True
ALLOWED_HOSTS = [
    "*",
    "banco.academiaroberthooke.com",
    "office.academiaroberthooke.com",
    "192.168.18.20",
]
# Redirecciones de login
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'

ONLYOFFICE_API_URL = "https://office.academiaroberthooke.com/web-apps/apps/api/documents/api.js"
ONLYOFFICE_CALLBACK_URL = "https://banco.academiaroberthooke.com/onlyoffice/callback/"
ONLYOFFICE_JWT_SECRET = "eeyuiJmUl1XI3FUz5gEf"
SITE_DOMAIN = "https://banco.academiaroberthooke.com"
FILE_UPLOAD_PERMISSIONS = 0o664

# Aplicaciones
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Preguntas',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URLs y WSGI
ROOT_URLCONF = 'PregRh.urls'
WSGI_APPLICATION = 'PregRh.wsgi.application'

# Plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_banco_preguntas',
        'USER': 'root',
        'PASSWORD': 'tu_password_seguro_root',
        'HOST': 'db_central',
        'PORT': '3306',
    }
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'pdf_conversion.log',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'Pregunta.views': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalización
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Campo automático por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- SEGURIDAD HTTPS ---
CSRF_TRUSTED_ORIGINS = [
    'https://banco.academiaroberthooke.com',
    "https://office.academiaroberthooke.com",
    'http://office.academiaroberthooke.com',
    'http://192.168.18.20:8003',
]

X_FRAME_OPTIONS = 'ALLOWALL'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
