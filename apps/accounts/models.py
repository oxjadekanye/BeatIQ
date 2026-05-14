import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.models import TimeStampedModel


class User(AbstractUser):
    """Primary auth identity for BeatIQ (JWT)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    email_verified_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        help_text="When set, the user completed email verification.",
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "accounts_user"


class UserProfile(TimeStampedModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    display_name = models.CharField(max_length=255, blank=True)
    birth_year = models.PositiveSmallIntegerField(null=True, blank=True)
    birth_month = models.PositiveSmallIntegerField(null=True, blank=True)
    avatar_url = models.URLField(max_length=500, blank=True)
    bio = models.TextField(blank=True)
    country_code = models.CharField(max_length=2, blank=True)
    preferences = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "accounts_user_profile"

    def __str__(self):
        return self.display_name or str(self.user_id)
