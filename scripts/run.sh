#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Loading initial data (skips if already present)..."
python manage.py load_initial_data

# Create a superuser from env vars if one does not yet exist.
SUPERUSER_USER="${DJANGO_SUPERUSER_USER:-}"
SUPERUSER_EMAIL="${DJANGO_SUPERUSER_EMAIL:-}"
SUPERUSER_PASSWORD="${DJANGO_SUPERUSER_PASSWORD:-}"
if [ -n "$SUPERUSER_USER" ] && [ -n "$SUPERUSER_EMAIL" ] && [ -n "$SUPERUSER_PASSWORD" ]; then
  python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if User.objects.filter(username="$SUPERUSER_USER").exists():
    print("Superuser already exists — skipping.")
else:
    User.objects.create_superuser("$SUPERUSER_USER", "$SUPERUSER_EMAIL", "$SUPERUSER_PASSWORD")
    print("Superuser '$SUPERUSER_USER' created.")
EOF
fi

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting gunicorn..."
exec gunicorn mario_portfolio.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers ${GUNICORN_WORKERS:-2} \
    --access-logfile - \
    --error-logfile -