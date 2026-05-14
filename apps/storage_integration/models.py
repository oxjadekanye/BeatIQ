from django.conf import settings
from django.db import models

from apps.core.models import UUIDTimeStampedModel


class StorageProvider(UUIDTimeStampedModel):
    class BackendKind(models.TextChoices):
        S3 = "s3", "Amazon S3"
        GCS = "gcs", "Google Cloud Storage"
        AZURE = "azure", "Azure Blob"
        OTHER = "other", "Other"

    code = models.SlugField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    backend_kind = models.CharField(
        max_length=16,
        choices=BackendKind.choices,
        default=BackendKind.S3,
    )
    config = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "storage_provider"

    def __str__(self):
        return self.name


class ManagedStorageObject(UUIDTimeStampedModel):
    provider = models.ForeignKey(
        StorageProvider,
        on_delete=models.PROTECT,
        related_name="objects",
    )
    object_key = models.CharField(max_length=1024, db_index=True)
    bucket_name = models.CharField(max_length=255, blank=True)
    media_type = models.CharField(max_length=128, blank=True)
    size_bytes = models.BigIntegerField(null=True, blank=True)
    checksum_sha256 = models.CharField(max_length=128, blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="storage_objects",
    )

    class Meta:
        db_table = "storage_managed_object"
        unique_together = ("provider", "object_key")

    def __str__(self):
        return self.object_key
