"""Local development settings."""
from .base import *  # noqa: F401, F403

DEBUG = True
ALLOWED_HOSTS = ['*']
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
