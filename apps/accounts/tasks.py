import logging

from celery import shared_task
from django.conf import settings

logger = logging.getLogger("beatiq.accounts")


@shared_task(bind=False, name="accounts.send_verification_email")
def send_verification_email_task(user_id: str, verify_url: str) -> None:
    from apps.accounts.models import User
    from apps.accounts.services.email_verification import send_verification_email

    user = User.objects.get(pk=user_id)
    send_verification_email(user, verify_url=verify_url)
    logger.info("verification_email_sent user_id=%s", user_id)


@shared_task(bind=False, name="accounts.send_welcome_email")
def send_welcome_email_task(user_id: str) -> None:
    from apps.accounts.models import User
    from apps.accounts.services.email_verification import send_welcome_email

    user = User.objects.get(pk=user_id)
    send_welcome_email(user)
    logger.info("welcome_email_sent user_id=%s", user_id)
