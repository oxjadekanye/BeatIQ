from django.conf import settings
from django.db import models

from apps.catalog.models import Track
from apps.core.models import UUIDTimeStampedModel


class SocialLinkMetadata(UUIDTimeStampedModel):
    """
    Cached resolution for share URLs (title/artist hints).
    Must not be used to facilitate stream ripping — store public metadata only.
    """

    class Platform(models.TextChoices):
        UNKNOWN = "unknown", "Unknown"
        PARTNER = "partner", "Verified partner share"
        OTHER = "other", "Other"

    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="social_link_metadata",
    )
    raw_url = models.URLField(max_length=800)
    normalized_url = models.URLField(max_length=800, blank=True)
    platform = models.CharField(
        max_length=32,
        choices=Platform.choices,
        default=Platform.UNKNOWN,
        db_index=True,
    )
    detected_title = models.CharField(max_length=255, blank=True)
    detected_artist = models.CharField(max_length=255, blank=True)
    confidence = models.FloatField(default=0.0)
    resolved_track = models.ForeignKey(
        Track,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="social_resolutions",
    )
    raw_metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "social_metadata_link"
        indexes = [
            models.Index(fields=("normalized_url",)),
        ]
