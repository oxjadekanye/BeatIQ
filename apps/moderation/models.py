from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.core.models import UUIDTimeStampedModel


class ModerationReport(UUIDTimeStampedModel):
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        IN_REVIEW = "in_review", "In review"
        RESOLVED = "resolved", "Resolved"
        DISMISSED = "dismissed", "Dismissed"

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="moderation_reports_filed",
    )
    reason_code = models.CharField(max_length=64, db_index=True)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.OPEN,
        db_index=True,
    )
    subject_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    subject_object_id = models.CharField(max_length=64)
    subject = GenericForeignKey("subject_content_type", "subject_object_id")

    class Meta:
        db_table = "moderation_report"
        indexes = [
            models.Index(fields=("status", "created_at")),
        ]


class ModerationAction(UUIDTimeStampedModel):
    class ActionType(models.TextChoices):
        NOTE = "note", "Note"
        ESCALATE = "escalate", "Escalate"
        APPROVE_ASSET = "approve_asset", "Approve asset"
        REJECT_ASSET = "reject_asset", "Reject asset"
        SUSPEND_USER = "suspend_user", "Suspend user"

    report = models.ForeignKey(
        ModerationReport,
        on_delete=models.CASCADE,
        related_name="actions",
    )
    moderator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="moderation_actions",
    )
    action_type = models.CharField(max_length=32, choices=ActionType.choices)
    note = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "moderation_action"
