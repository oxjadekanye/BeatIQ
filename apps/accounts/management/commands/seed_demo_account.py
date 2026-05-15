"""Create or update the two standard BeatIQ accounts (verified email) for local/staging use."""

from django.core.management.base import BaseCommand

from apps.accounts.models import User, UserProfile
from apps.accounts.services.account_activation import activate_user_for_login, normalize_email


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
    normalized_email = normalize_email(email)
    user, created = User.objects.get_or_create(
        email=normalized_email,
        defaults={
            "username": base_username,
            "first_name": first_name[:150],
            "last_name": last_name[:150],
            "is_active": True,
        },
    )
    if not created:
        user.username = user.username or base_username
    user.first_name = first_name[:150]
    user.last_name = last_name[:150]
    user.set_password(password)
    user.is_active = True
    user.save()
    activate_user_for_login(user, verify_email=True)
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.display_name = display_name
    profile.birth_year = birth_year
    profile.birth_month = birth_month
    profile.save()


class Command(BaseCommand):
    help = (
        "Ensures two standard accounts exist (verified email): Xavier Adekanye and Inumidun Bakare."
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
                "email": "inumidunbakare@gmail.com",
                "password": "Aderoju1122@",
                "first_name": "Inumidun",
                "last_name": "Bakare",
                "display_name": "Inumidun Bakare",
                "birth_year": 1992,
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
