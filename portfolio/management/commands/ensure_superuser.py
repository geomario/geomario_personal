import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Create a superuser from DJANGO_SUPERUSER_USER, DJANGO_SUPERUSER_EMAIL and "
        "DJANGO_SUPERUSER_PASSWORD. Does nothing if any is unset or the user exists."
    )

    def handle(self, *args, **options):
        # Read straight from the environment so the values never pass through
        # shell or Python source, whatever characters they contain.
        username = os.environ.get("DJANGO_SUPERUSER_USER", "")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")
        if not (username and email and password):
            self.stdout.write("DJANGO_SUPERUSER_* not fully set — skipping superuser creation.")
            return

        User = get_user_model()
        if User.objects.filter(username=username).exists():
            self.stdout.write("Superuser already exists — skipping.")
            return

        User.objects.create_superuser(username, email, password)
        self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created."))
