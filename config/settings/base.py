"""Base settings shared by local and production."""
import os
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = BASE_DIR / 'main'

env = environ.Env()

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=False)
SECRET_KEY = env('DJANGO_SECRET_KEY', default='dev-secret-not-for-production')
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['*'])
CSRF_TRUSTED_ORIGINS = env.list('DJANGO_CSRF_TRUSTED_ORIGINS', default=[])

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_TZ = True

# DATABASE
# ------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': env('SQLITE_PATH', default=str(BASE_DIR / 'db.sqlite3')),
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# URLS
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# APPS
# ------------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    'django_jinja',
    'django_htmx',
    'main',
    'main.pizza_orders',
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]

# SESSIONS
# ------------------------------------------------------------------------------
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_SAVE_EVERY_REQUEST = True

# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django_jinja.jinja2.Jinja2',
        'DIRS': [APPS_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'match_extension': '.jinja',
            'context_processors': [
                'django.template.context_processors.request',
            ],
            'globals': {
                'django_htmx_script': 'django_htmx.jinja.django_htmx_script',
            },
        },
    },
]

# STATIC
# ------------------------------------------------------------------------------
STATIC_ROOT = str(BASE_DIR / 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# SECURITY (basic)
# ------------------------------------------------------------------------------
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'

# External APIs
# ------------------------------------------------------------------------------
GROQ_API_KEY = env('GROQ_API_KEY', default='')
# Make available to litellm
os.environ.setdefault('GROQ_API_KEY', GROQ_API_KEY)

# Pick any Groq model: https://console.groq.com/docs/models
# litellm prefixes Groq models with `groq/`.
LLM_MODEL = env('LLM_MODEL', default='groq/openai/gpt-oss-20b')
