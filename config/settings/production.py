"""
BeatIQ production settings (Render, VPS, etc.).

PostgreSQL via DATABASE_URL is required — SQLite is rejected here (see ImproperlyConfigured
below) so missing DB config cannot silently break login with HTTP 500.

When `RENDER` or `RENDER_EXTERNAL_URL` is set, DEBUG is forced off and SECRET_KEY is validated.
Demo/seed commands are never run automatically — invoke manually via management commands.
"""

import os
from urllib.parse import urlparse

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403, F401

# --- DEBUG: never expose Django debug pages on Render ---
_on_render = os.environ.get("RENDER", "").lower() in ("true", "1", "yes") or bool(
    os.environ.get("RENDER_EXTERNAL_URL", "").strip(),
)
_env_debug = os.environ.get("DEBUG", "False").lower() in ("1", "true", "yes")
if _on_render:
    DEBUG = False  # noqa: F405
else:
    DEBUG = _env_debug  # noqa: F405

# --- Secrets: never use template defaults on Render ---
if _on_render:
    _sk = (os.environ.get("SECRET_KEY") or "").strip()  # noqa: F405
    if not _sk or _sk == "unsafe-dev-only-change-in-env":
        raise ImproperlyConfigured(
            "BeatIQ on Render requires a strong SECRET_KEY environment variable.",
        )

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

# --- Database: PostgreSQL required (never silent SQLite in production) ---
# Missing DATABASE_URL falls back to SQLite in base.py — empty file on Render → "no such table"
# on login. Fail fast with a clear message unless explicitly opted in for local prod experiments.
_db = DATABASES["default"]  # noqa: F405
_engine = str(_db.get("ENGINE") or "")
_is_sqlite = _engine.endswith("sqlite3")
if _is_sqlite and os.environ.get("BEATIQ_ALLOW_SQLITE_PRODUCTION", "").lower() not in (
    "1",
    "true",
    "yes",
):
    raise ImproperlyConfigured(
        "BeatIQ production requires PostgreSQL. DATABASE_URL is missing or invalid, so Django "
        "would use SQLite (no migrations / empty DB → login HTTP 500). On Render: create a "
        "PostgreSQL instance, link it to this web service so DATABASE_URL is set, set "
        "DJANGO_SETTINGS_MODULE=config.settings.production, and ensure the release phase runs "
        "`python manage.py migrate`. For rare local tests only, set BEATIQ_ALLOW_SQLITE_PRODUCTION=1."
    )

if _on_render and not os.environ.get("DATABASE_URL", "").strip():
    raise ImproperlyConfigured(
        "BeatIQ on Render requires DATABASE_URL (link the Render PostgreSQL instance to the web service).",
    )

# --- Hosts / CSRF (browser admin + future web clients) ---
_ensure_local_hosts = ("localhost", "127.0.0.1")
for _h in _ensure_local_hosts:
    if _h not in ALLOWED_HOSTS:  # noqa: F405
        ALLOWED_HOSTS = [*ALLOWED_HOSTS, _h]  # noqa: F405

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

EMAIL_HOST = (os.environ.get("EMAIL_HOST") or "").strip()
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True").lower() in ("1", "true", "yes")
# Avoid hanging TCP connects during API requests (e.g. registration) when SMTP is missing or wrong.
EMAIL_TIMEOUT = int(os.environ.get("EMAIL_TIMEOUT", "12"))
_email_backend = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
if "smtp" in _email_backend and not EMAIL_HOST:
    EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"
else:
    EMAIL_BACKEND = _email_backend
