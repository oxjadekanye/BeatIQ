"""
Idempotent local superuser helper.

Usage (after migrate):
  BEATIQ_SUPERUSER_EMAIL=admin@localhost BEATIQ_SUPERUSER_PASSWORD=secret \\
    python manage.py beatiq_createsuperuser

Defaults are dev-only; override in production via env.
"""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = "Create a superuser from BEATIQ_SUPERUSER_* environment variables if missing."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force-email-verified",
            action="store_true",
            help="Set email_verified_at on the user (recommended for local JWT testing).",
        )

    def handle(self, *args, **options):
        User = get_user_model()
        email = os.environ.get("BEATIQ_SUPERUSER_EMAIL", "admin@localhost").strip().lower()
        password = os.environ.get("BEATIQ_SUPERUSER_PASSWORD", "adminchangeme")
        username = os.environ.get("BEATIQ_SUPERUSER_USERNAME", "admin").strip() or email.split("@")[0]

        existing = User.objects.filter(email__iexact=email).first()
        if existing:
            if options["force_email_verified"] and not existing.email_verified_at:
                existing.email_verified_at = timezone.now()
                existing.save(update_fields=["email_verified_at"])
                self.stdout.write(self.style.SUCCESS(f"Updated email_verified_at for {email}"))
            else:
                self.stdout.write(self.style.WARNING(f"User already exists: {email}"))
            return

        user = User.objects.create_superuser(
            username=username[:150],
            email=email,
            password=password,
        )
        user.email_verified_at = timezone.now()
        user.save(update_fields=["email_verified_at"])
        self.stdout.write(self.style.SUCCESS(f"Created superuser {email} (username={user.username})"))
