#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Loading initial data (skips if already present)..."
python manage.py load_initial_data

echo "Creating superuser from DJANGO_SUPERUSER_* (skips if unset or present)..."
python manage.py ensure_superuser

echo "Starting gunicorn..."
exec gunicorn mario_portfolio.wsgi:application \
    --bind "0.0.0.0:${PORT:-8000}" \
    --workers "${GUNICORN_WORKERS:-2}" \
    --no-control-socket \
    --access-logfile - \
    --error-logfile -