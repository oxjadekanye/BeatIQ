from django.conf import settings
from django.db import models

from apps.core.models import UUIDTimeStampedModel


class AIMoodDiscoverySession(UUIDTimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        READY = "ready", "Ready"
        FAILED = "failed", "Failed"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mood_sessions",
    )
    mood_label = models.CharField(max_length=64, blank=True)
    mood_vector = models.JSONField(default=dict, blank=True)
    matched_track_ids = models.JSONField(default=list, blank=True)
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    provider_job_id = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "ai_services_mood_session"


class AIRecognitionPrepJob(UUIDTimeStampedModel):
    """
    Prepares metadata for legal audio identification (e.g. user-owned clip or partner feed).
    Does not implement stream ripping or DRM bypass.
    """

    class Status(models.TextChoices):
        QUEUED = "queued", "Queued"
        PROCESSING = "processing", "Processing"
        DONE = "done", "Done"
        FAILED = "failed", "Failed"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recognition_prep_jobs",
    )
    input_storage_object = models.ForeignKey(
        "storage_integration.ManagedStorageObject",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recognition_prep_jobs",
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.QUEUED,
        db_index=True,
    )
    fingerprint_handle = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "ai_services_recognition_prep_job"
