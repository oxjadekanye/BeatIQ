"""Shared helpers for activating BeatIQ user accounts (login-ready)."""

from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


def normalize_email(email: str) -> str:
    return email.strip().lower()


def activate_user_for_login(user, *, verify_email: bool = True) -> list[str]:
    """Ensure a user can sign in. Returns list of fields that were updated."""
    update_fields: list[str] = []
    if not user.is_active:
        user.is_active = True
        update_fields.append("is_active")
    if verify_email and not user.email_verified_at:
        user.email_verified_at = timezone.now()
        update_fields.append("email_verified_at")
    if update_fields:
        user.save(update_fields=update_fields)
    return update_fields
