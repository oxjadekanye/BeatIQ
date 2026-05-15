"""Signed tokens and outbound mail for email verification."""

from __future__ import annotations

import logging

from django.conf import settings
from django.core.mail import send_mail
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner

from apps.accounts.models import User

logger = logging.getLogger("beatiq.accounts")

SIGN_SALT = "beatiq-email-verify"


def build_verification_token(user_id: str) -> str:
    signer = TimestampSigner(salt=SIGN_SALT)
    return signer.sign(user_id)


def parse_verification_token(token: str, max_age_seconds: int) -> str | None:
    signer = TimestampSigner(salt=SIGN_SALT)
    try:
        return signer.unsign(token, max_age=max_age_seconds)
    except (BadSignature, SignatureExpired) as exc:
        logger.info("email_verify_token_invalid: %s", exc)
        return None


def send_verification_email(user: User, *, verify_url: str) -> None:
    subject = "Verify your BeatIQ email"
    body = (
        "Welcome to BeatIQ — Find Every Beat.\n\n"
        f"Confirm your email by opening this link (or paste into your browser):\n{verify_url}\n\n"
        "If you did not create an account, you can ignore this message.\n"
    )
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or getattr(settings, "EMAIL_HOST_USER", None)
    if not from_email:
        logger.warning("verification_email_skipped_no_from_email user_id=%s", user.pk)
        return
    try:
        send_mail(
            subject,
            body,
            from_email,
            [user.email],
            fail_silently=False,
        )
    except Exception as exc:
        # Never fail registration HTTP: Celery eager / no broker runs this in-request.
        logger.exception("verification_email_failed user_id=%s: %s", user.pk, exc)


def send_welcome_email(user: User) -> None:
    subject = "Welcome to BeatIQ"
    body = (
        "Your email is verified — thanks for joining BeatIQ.\n\n"
        "Find every beat: your library, playlists, and downloads stay private to your account.\n\n"
        "Happy listening,\nThe BeatIQ team\n"
    )
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or getattr(settings, "EMAIL_HOST_USER", None)
    if not from_email:
        logger.warning("welcome_email_skipped_no_from_email user_id=%s", user.pk)
        return
    try:
        send_mail(
            subject,
            body,
            from_email,
            [user.email],
            fail_silently=False,
        )
    except Exception as exc:
        logger.exception("welcome_email_failed user_id=%s: %s", user.pk, exc)
