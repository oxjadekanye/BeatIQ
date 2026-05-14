#!/usr/bin/env bash
# Render release phase: apply migrations (runs with DATABASE_URL available).
set -euo pipefail
export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.production}"
python manage.py migrate --noinput
