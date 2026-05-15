"""Create or repair a BeatIQ login account (production/staging ops)."""

import os

from django.core.management.base import BaseCommand, CommandError

from apps.accounts.models import User, UserProfile
from apps.accounts.services.account_activation import activate_user_for_login, normalize_email


class Command(BaseCommand):
    help = (
        "Ensure a user exists and can sign in (is_active, optional verified email, password reset). "
        "Example: python manage.py ensure_user_account inumidunbakare@gmail.com --verify-email "
        "--password-env BEATIQ_USER_PASSWORD"
    )

    def add_arguments(self, parser):
        parser.add_argument("email", type=str, help="User email address")
        parser.add_argument(
            "--password",
            type=str,
            help="Set account password (prefer --password-env on servers)",
        )
        parser.add_argument(
            "--password-env",
            type=str,
            default="",
            help="Read password from this environment variable",
        )
        parser.add_argument(
            "--verify-email",
            action="store_true",
            help="Mark email as verified so login is allowed when verification is required",
        )
        parser.add_argument(
            "--display-name",
            type=str,
            default="",
            help="Profile display name when creating a new user",
        )

    def handle(self, *args, **options):
        email = normalize_email(options["email"])
        if not email:
            raise CommandError("Email is required.")

        password = (options.get("password") or "").strip()
        env_key = (options.get("password_env") or "").strip()
        if env_key:
            password = (os.environ.get(env_key) or "").strip()
        if not password:
            raise CommandError("Provide --password or --password-env with a non-empty value.")

        display_name = (options.get("display_name") or "").strip()
        username = email.split("@", 1)[0][:150]

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": username,
                "is_active": True,
            },
        )
        if created:
            self.stdout.write(self.style.WARNING(f"Created new user: {email}"))
        else:
            self.stdout.write(f"Updating existing user: {email}")

        user.username = user.username or username
        user.set_password(password)
        user.is_active = True
        user.save()

        activate_user_for_login(user, verify_email=bool(options["verify_email"]))

        profile, _ = UserProfile.objects.get_or_create(user=user)
        if display_name:
            profile.display_name = display_name
            profile.save(update_fields=["display_name"])

        self.stdout.write(
            self.style.SUCCESS(
                f"Account ready: {email} "
                f"(active={user.is_active}, verified={bool(user.email_verified_at)})",
            ),
        )
