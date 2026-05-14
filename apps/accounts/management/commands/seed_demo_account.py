"""Create or update the two standard BeatIQ demo accounts (verified email) for local testing."""

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.accounts.models import User, UserProfile


def _upsert_user(
    *,
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    display_name: str,
    birth_year: int,
    birth_month: int,
    username_hint: str,
) -> None:
    base_username = username_hint[:150]
    user, created = User.objects.get_or_create(
        email=email.lower().strip(),
        defaults={
            "username": base_username,
            "first_name": first_name[:150],
            "last_name": last_name[:150],
        },
    )
    if not created:
        user.username = user.username or base_username
    user.first_name = first_name[:150]
    user.last_name = last_name[:150]
    user.set_password(password)
    user.email_verified_at = timezone.now()
    user.save()
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.display_name = display_name
    profile.birth_year = birth_year
    profile.birth_month = birth_month
    profile.save()


class Command(BaseCommand):
    help = (
        "Ensures two standard accounts exist (verified): Xavier Adekanye and Meedun Adekanye."
    )

    def handle(self, *args, **options):
        accounts = [
            {
                "email": "oxj.adekanye@gmail.com",
                "password": "Aderoju1122@",
                "first_name": "Xavier",
                "last_name": "Adekanye",
                "display_name": "Xavier Adekanye",
                "birth_year": 1982,
                "birth_month": 12,
                "username_hint": "oxj_adekanye",
            },
            {
                "email": "inumidunbakare@yahoo.com",
                "password": "Aderoju1122@",
                "first_name": "Meedun",
                "last_name": "Adekanye",
                "display_name": "Meedun Adekanye",
                "birth_year": 1991,
                "birth_month": 6,
                "username_hint": "inumidunbakare",
            },
        ]
        for spec in accounts:
            _upsert_user(**spec)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Account ready: {spec['email']} ({spec['display_name']}, "
                    f"DOB {spec['birth_month']:02d}/{spec['birth_year']})",
                ),
            )
