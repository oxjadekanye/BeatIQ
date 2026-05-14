import os

from .base import *  # noqa: F403

# Strong default for local JWT signing when SECRET_KEY is unset (do not use in production).
if not os.environ.get("SECRET_KEY"):  # noqa: F405
    SECRET_KEY = "django-insecure-local-dev-" + ("x" * 48)  # noqa: F405

DEBUG = True
ALLOWED_HOSTS = ["*"]

# Local dev: SQLite by default (set USE_SQLITE=false to use DATABASE_URL / Postgres from base).
_use_sqlite = os.environ.get("USE_SQLITE", "true").lower() in ("1", "true", "yes")
if _use_sqlite:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(BASE_DIR / "db.sqlite3"),  # noqa: F405
        }
    }

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# Relaxed CORS for local Flutter / web during development
CORS_ALLOW_ALL_ORIGINS = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
