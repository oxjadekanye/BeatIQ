from django.conf import settings
from django.db import models

from apps.core.models import UUIDTimeStampedModel


class CreatorProfile(UUIDTimeStampedModel):
    class VerificationStatus(models.TextChoices):
        UNVERIFIED = "unverified", "Unverified"
        PENDING = "pending", "Pending"
        VERIFIED = "verified", "Verified"
        SUSPENDED = "suspended", "Suspended"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="creator_profile",
    )
    display_name = models.CharField(max_length=255)
    verification_status = models.CharField(
        max_length=16,
        choices=VerificationStatus.choices,
        default=VerificationStatus.UNVERIFIED,
        db_index=True,
    )
    rights_attestation = models.TextField(
        blank=True,
        help_text="Creator attestation of rights; moderation review required.",
    )

    class Meta:
        db_table = "creators_profile"


class CreatorUploadBatch(UUIDTimeStampedModel):
    creator = models.ForeignKey(
        CreatorProfile,
        on_delete=models.CASCADE,
        related_name="batches",
    )
    title = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "creators_upload_batch"


class CreatorUploadAsset(UUIDTimeStampedModel):
    class ReviewStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    batch = models.ForeignKey(
        CreatorUploadBatch,
        on_delete=models.CASCADE,
        related_name="assets",
    )
    title = models.CharField(max_length=255)
    storage_object = models.ForeignKey(
        "storage_integration.ManagedStorageObject",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="creator_upload_assets",
    )
    review_status = models.CharField(
        max_length=16,
        choices=ReviewStatus.choices,
        default=ReviewStatus.PENDING,
        db_index=True,
    )

    class Meta:
        db_table = "creators_upload_asset"
