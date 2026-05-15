import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger("beatiq.accounts")

ADMIN_SIGNUP_NOTIFY_EMAIL = "admin@beatiq.co.uk"


def send_admin_new_user_signup_email(user) -> None:
    """Notify BeatIQ admin when a new account is created (best-effort; must not break registration)."""
    subject = f"[BeatIQ] New user signup: {user.email}"
    body = (
        "A new BeatIQ account was created via the app or API.\n\n"
        f"Email: {user.email}\n"
        f"User ID: {user.pk}\n"
        f"Name: {user.get_full_name()}\n"
        f"Username: {user.username}\n"
    )
    from_email = (getattr(settings, "DEFAULT_FROM_EMAIL", None) or "").strip()
    if not from_email:
        from_email = (getattr(settings, "EMAIL_HOST_USER", None) or "").strip()
    if not from_email:
        logger.warning("admin_signup_email_skipped_missing_DEFAULT_FROM_EMAIL")
        return
    try:
        send_mail(
            subject,
            body,
            from_email,
            [ADMIN_SIGNUP_NOTIFY_EMAIL],
            fail_silently=True,
        )
        logger.info("admin_signup_notification_sent for user_id=%s", user.pk)
    except Exception:
        logger.exception("admin_signup_notification_failed user_id=%s", user.pk)
