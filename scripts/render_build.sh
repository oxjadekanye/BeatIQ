#!/usr/bin/env bash
# Render / CI: install deps and collect static files (no DB migrations here).
set -euo pipefail
export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.production}"
pip install -r requirements.txt
python manage.py collectstatic --noinput
