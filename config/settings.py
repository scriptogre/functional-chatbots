from pathlib import Path

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
APPS_DIR = ROOT_DIR / "functional_chatbots"
TEMPLATES_DIR = APPS_DIR / "templates"

DEBUG = True
ALLOWED_HOSTS = ["*"]
IGNORABLE_404_URLS = [r'^favicon\.ico$']
ROOT_URLCONF = 'config.urls'
SECRET_KEY = "pizza"

INSTALLED_APPS = [
    # To enable serving static files
    "django.contrib.staticfiles",

    # To enable sessions
    "django.contrib.sessions",

    # Local apps
    "functional_chatbots",
]

# TEMPLATES = []  # We use JinjaX - configuration in `config/jinjax.py`

# https://docs.djangoproject.com/en/5.0/topics/http/sessions/
MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
]
# https://docs.djangoproject.com/en/5.0/topics/http/sessions/#using-cached-sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# https://docs.djangoproject.com/en/5.0/howto/static-files/#configuring-static-files
STATIC_URL = "static/"
