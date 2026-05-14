from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.catalog.models import Track
from apps.core.models import UUIDTimeStampedModel


class SavedDownload(UUIDTimeStampedModel):
    """
    Record of a user download fulfilled through a partner-authorized channel.
    File bytes are referenced via cloud storage integration, never ripped streams.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="saved_downloads",
    )
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="saved_downloads")
    licensed_track_source = models.ForeignKey(
        "licensing.LicensedTrackSource",
        on_delete=models.PROTECT,
        related_name="saved_downloads",
    )
    permission_snapshot = models.JSONField(
        default=dict,
        help_text="Immutable snapshot of DownloadPermission facts at issuance time.",
    )
    storage_object = models.ForeignKey(
        "storage_integration.ManagedStorageObject",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="saved_downloads",
    )
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "downloads_saved_download"
        indexes = [
            models.Index(fields=("user", "track")),
        ]


class DownloadAuditLog(UUIDTimeStampedModel):
    class Action(models.TextChoices):
        REQUESTED = "requested", "Requested"
        ALLOWED = "allowed", "Allowed"
        DENIED = "denied", "Denied"
        COMPLETED = "completed", "Completed"
        REVOKED = "revoked", "Revoked"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="download_audit_logs",
    )
    track = models.ForeignKey(
        Track,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="download_audit_logs",
    )
    licensed_track_source = models.ForeignKey(
        "licensing.LicensedTrackSource",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="download_audit_logs",
    )
    action = models.CharField(max_length=32, choices=Action.choices, db_index=True)
    success = models.BooleanField(default=False, db_index=True)
    reason_code = models.CharField(max_length=64, blank=True)
    detail = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=512, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "downloads_download_audit_log"
        ordering = ("-created_at",)


class OfflineLibraryItem(UUIDTimeStampedModel):
    """Device-scoped offline entitlement mirror (client sync)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="offline_items",
    )
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="offline_items")
    device_id = models.CharField(max_length=128, db_index=True)
    saved_download = models.ForeignKey(
        SavedDownload,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="offline_items",
    )
    removed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "downloads_offline_library_item"
        unique_together = ("user", "track", "device_id")


class ComplianceAuditLog(UUIDTimeStampedModel):
    """Cross-domain compliance events (AI jobs, moderation, subscription changes)."""

    class EventType(models.TextChoices):
        AI_JOB = "ai_job", "AI job"
        SUBSCRIPTION = "subscription", "Subscription"
        MODERATION = "moderation", "Moderation"
        STORAGE = "storage", "Storage"
        OTHER = "other", "Other"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="compliance_audit_logs",
    )
    event_type = models.CharField(max_length=32, choices=EventType.choices, db_index=True)
    subject_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    subject_object_id = models.CharField(max_length=64, blank=True)
    subject = GenericForeignKey("subject_content_type", "subject_object_id")
    payload = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = "downloads_compliance_audit_log"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=("event_type", "created_at")),
        ]
