"""Celery tasks for AI pipelines (vendor integration stubs)."""

from __future__ import annotations

import logging
import uuid

from celery import shared_task
from django.utils import timezone

logger = logging.getLogger("beatiq.ai")


@shared_task(name="ai_services.playlist_recommendation")
def playlist_recommendation_task(recommendation_id: str) -> str:
    from apps.downloads.models import ComplianceAuditLog
    from apps.downloads.services.audit import log_compliance_event
    from apps.playlists.models import AIPlaylistRecommendation

    rec = AIPlaylistRecommendation.objects.select_related("user").get(pk=recommendation_id)
    job_id = str(uuid.uuid4())
    rec.provider_job_id = job_id
    rec.save(update_fields=["provider_job_id", "updated_at"])

    log_compliance_event(
        user=rec.user,
        event_type=ComplianceAuditLog.EventType.AI_JOB,
        subject=rec,
        payload={
            "job": "playlist_recommendation",
            "correlation_id": job_id,
            "celery_task": "ai_services.playlist_recommendation",
        },
    )

    seeds = list(rec.seed_track_ids or [])[:50]
    rec.recommended_track_ids = seeds[:20] if seeds else []
    rec.explanation = "Placeholder: connect `AIProviderClient` to your recommender."
    rec.status = AIPlaylistRecommendation.Status.READY
    rec.save(update_fields=["recommended_track_ids", "explanation", "status", "updated_at"])
    logger.info("playlist_recommendation_done id=%s job_id=%s", recommendation_id, job_id)
    return job_id


@shared_task(name="ai_services.mood_discovery")
def mood_discovery_task(session_id: str) -> str:
    from apps.ai_services.models import AIMoodDiscoverySession
    from apps.downloads.models import ComplianceAuditLog
    from apps.downloads.services.audit import log_compliance_event

    session = AIMoodDiscoverySession.objects.select_related("user").get(pk=session_id)
    job_id = str(uuid.uuid4())
    session.provider_job_id = job_id
    session.save(update_fields=["provider_job_id", "updated_at"])

    log_compliance_event(
        user=session.user,
        event_type=ComplianceAuditLog.EventType.AI_JOB,
        subject=session,
        payload={
            "job": "mood_discovery",
            "correlation_id": job_id,
            "celery_task": "ai_services.mood_discovery",
        },
    )

    session.matched_track_ids = []
    session.status = AIMoodDiscoverySession.Status.READY
    session.save(update_fields=["matched_track_ids", "status", "updated_at"])
    logger.info("mood_discovery_done id=%s job_id=%s", session_id, job_id)
    return job_id


@shared_task(name="ai_services.recognition_prep")
def recognition_prep_task(job_id: str) -> str:
    from apps.ai_services.models import AIRecognitionPrepJob
    from apps.downloads.models import ComplianceAuditLog
    from apps.downloads.services.audit import log_compliance_event

    job = AIRecognitionPrepJob.objects.select_related("user").get(pk=job_id)
    correlation = str(uuid.uuid4())
    log_compliance_event(
        user=job.user,
        event_type=ComplianceAuditLog.EventType.AI_JOB,
        subject=job,
        payload={
            "job": "recognition_prep",
            "correlation_id": correlation,
            "input_object_id": str(job.input_storage_object_id)
            if job.input_storage_object_id
            else None,
            "celery_task": "ai_services.recognition_prep",
        },
    )

    job.fingerprint_handle = f"stub:{correlation}"
    job.status = AIRecognitionPrepJob.Status.DONE
    job.save(update_fields=["fingerprint_handle", "status", "updated_at"])
    logger.info("recognition_prep_done id=%s correlation=%s", job_id, correlation)
    return correlation
