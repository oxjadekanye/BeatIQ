import logging

from apps.downloads.models import ComplianceAuditLog, DownloadAuditLog

logger = logging.getLogger("beatiq.audit")


def log_download_event(
    *,
    user,
    track,
    licensed_track_source,
    action: str,
    success: bool,
    reason_code: str = "",
    detail: str = "",
    request=None,
    metadata=None,
):
    meta = metadata or {}
    ip = None
    ua = ""
    if request is not None:
        ip = request.META.get("REMOTE_ADDR")
        ua = (request.META.get("HTTP_USER_AGENT") or "")[:512]
    DownloadAuditLog.objects.create(
        user=user,
        track=track,
        licensed_track_source=licensed_track_source,
        action=action,
        success=success,
        reason_code=reason_code[:64],
        detail=detail[:2000],
        ip_address=ip,
        user_agent=ua,
        metadata=meta,
    )
    logger.info(
        "download_audit action=%s success=%s user=%s track=%s reason=%s",
        action,
        success,
        getattr(user, "id", None),
        getattr(track, "id", None),
        reason_code,
    )


def log_compliance_event(
    *,
    user=None,
    event_type: str,
    subject=None,
    payload=None,
    request=None,
):
    from django.contrib.contenttypes.models import ContentType

    ct = None
    oid = ""
    if subject is not None:
        ct = ContentType.objects.get_for_model(subject.__class__)
        oid = str(subject.pk)
    ip = request.META.get("REMOTE_ADDR") if request else None
    ComplianceAuditLog.objects.create(
        user=user,
        event_type=event_type,
        subject_content_type=ct,
        subject_object_id=oid,
        payload=payload or {},
        ip_address=ip,
    )
