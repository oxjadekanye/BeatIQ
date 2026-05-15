import logging

from celery import shared_task

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


@shared_task(bind=False, name="accounts.notify_admin_new_signup")
def notify_admin_new_signup_task(user_id: str) -> None:
    from apps.accounts.models import User
    from apps.accounts.services.admin_notifications import send_admin_new_user_signup_email

    user = User.objects.get(pk=user_id)
    send_admin_new_user_signup_email(user)
    logger.info("admin_signup_notification_enqueued user_id=%s", user_id)


def enqueue_or_apply_sync(task, args=(), kwargs=None):
    """
    Publish to Celery when a broker is available; otherwise run the task in-process.

    Render (and similar) often run the web service without Redis/workers. Unhandled broker
    errors during `.delay()` would turn registration into HTTP 500 after the user row exists.
    """
    kwargs = kwargs or {}
    try:
        task.delay(*args, **kwargs)
    except Exception:
        logger.warning(
            "celery_enqueue_failed_running_inline task=%s",
            getattr(task, "name", repr(task)),
            exc_info=True,
        )
        task.apply(args=args, kwargs=kwargs)
