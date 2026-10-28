"""
Django settings for the mario_portfolio project.

Content is stored in PostgreSQL and managed from /admin. Configuration
is environment-driven so the same image runs locally and in production.
"""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

DEV_SECRET_KEY = "dev-secret-key-change-me"


def env_list(name, default=""):
    return [item.strip() for item in os.environ.get(name, default).split(",") if item.strip()]


DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", DEV_SECRET_KEY)

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "*" if DEBUG else "")

# The development defaults above are only allowed with DEBUG on, so a
# production start without real values fails loudly instead of running unsafe.
if not DEBUG:
    if SECRET_KEY == DEV_SECRET_KEY or len(SECRET_KEY) < 50:
        raise ImproperlyConfigured(
            "Set DJANGO_SECRET_KEY to a random value of at least 50 characters when DJANGO_DEBUG=0."
        )
    if not ALLOWED_HOSTS or "*" in ALLOWED_HOSTS:
        raise ImproperlyConfigured(
            "Set DJANGO_ALLOWED_HOSTS to the site's host names when DJANGO_DEBUG=0."
        )

# HTTPS. Origins (e.g. https://example.com) allowed to POST forms such as the
# admin login; needed when the site is served under a different host or scheme.
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")
# Set to 1 only behind a proxy that terminates TLS and always sets
# X-Forwarded-Proto; otherwise clients could spoof it.
if os.environ.get("DJANGO_BEHIND_HTTPS_PROXY", "0") == "1":
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
# HSTS stays off until the site is confirmed to work over HTTPS: browsers
# cache it and refuse plain HTTP for the whole period.
SECURE_HSTS_SECONDS = int(os.environ.get("DJANGO_HSTS_SECONDS", "0"))

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "portfolio",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mario_portfolio.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mario_portfolio.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "postgres"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "postgres"),
        "HOST": os.environ.get("DB_HOST", "db"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

STATIC_URL = "static/"
STATIC_ROOT = "/vol/static"
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
