"""
BeatIQ production settings (Render, VPS, etc.).

When `RENDER` is set, `DATABASE_URL` must be present (link PostgreSQL on Render).
Demo/seed commands are never run automatically — invoke manually via management commands.
"""

import os
from urllib.parse import urlparse

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403, F401

DEBUG = os.environ.get("DEBUG", "False").lower() in ("1", "true", "yes")  # noqa: F405

# --- Render / reverse proxy ---
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "True").lower() in (
    "1",
    "true",
    "yes",
)

_hsts = int(os.environ.get("SECURE_HSTS_SECONDS", "0"))
if _hsts > 0:
    SECURE_HSTS_SECONDS = _hsts
    SECURE_HSTS_INCLUDE_SUBDOMAINS = (
        os.environ.get("SECURE_HSTS_INCLUDE_SUBDOMAINS", "False").lower() in ("1", "true", "yes")
    )
    SECURE_HSTS_PRELOAD = os.environ.get("SECURE_HSTS_PRELOAD", "False").lower() in ("1", "true", "yes")

# --- Database (Render PostgreSQL) ---
if os.environ.get("RENDER", "").lower() in ("true", "1", "yes") and not os.environ.get("DATABASE_URL"):
    raise ImproperlyConfigured(
        "BeatIQ on Render requires DATABASE_URL (link the Render PostgreSQL instance to the web service).",
    )

# --- Hosts / CSRF (browser admin + future web clients) ---
_render_external = os.environ.get("RENDER_EXTERNAL_URL", "").strip()
if _render_external:
    _rh = urlparse(_render_external).hostname
    if _rh and _rh not in ALLOWED_HOSTS:  # noqa: F405
        ALLOWED_HOSTS = [*ALLOWED_HOSTS, _rh]  # noqa: F405

_csrf_raw = os.environ.get("CSRF_TRUSTED_ORIGINS", "").strip()
if _csrf_raw:
    CSRF_TRUSTED_ORIGINS = [o.strip().rstrip("/") for o in _csrf_raw.split(",") if o.strip()]
elif _render_external.startswith("https://"):
    CSRF_TRUSTED_ORIGINS = [_render_external.rstrip("/")]

# --- CORS: never allow all origins in production; set explicit origins (web / tooling). ---
# Native Android OkHttp clients do not use browser CORS; this mainly affects browsers and WebViews.
CORS_ALLOW_ALL_ORIGINS = False

# --- Celery: real broker in production ---
CELERY_TASK_ALWAYS_EAGER = False

EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True").lower() in ("1", "true", "yes")
