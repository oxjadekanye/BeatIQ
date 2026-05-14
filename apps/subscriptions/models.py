from django.conf import settings
from django.db import models

from apps.core.models import UUIDTimeStampedModel


class Plan(UUIDTimeStampedModel):
    code = models.SlugField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    tier_order = models.PositiveSmallIntegerField(
        default=0,
        db_index=True,
        help_text="Higher unlocks more features (e.g. offline downloads).",
    )
    price_monthly_cents = models.PositiveIntegerField(default=0)
    stripe_price_id = models.CharField(max_length=255, blank=True)
    is_public = models.BooleanField(default=True)

    class Meta:
        db_table = "subscriptions_plan"
        ordering = ("tier_order", "code")

    def __str__(self):
        return self.name


class Subscription(UUIDTimeStampedModel):
    class Status(models.TextChoices):
        INCOMPLETE = "incomplete", "Incomplete"
        ACTIVE = "active", "Active"
        PAST_DUE = "past_due", "Past due"
        CANCELED = "canceled", "Canceled"
        TRIALING = "trialing", "Trialing"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name="subscriptions")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.INCOMPLETE,
        db_index=True,
    )
    current_period_start = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    cancel_at_period_end = models.BooleanField(default=False)
    external_customer_id = models.CharField(max_length=255, blank=True)
    external_subscription_id = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "subscriptions_subscription"
        indexes = [
            models.Index(fields=("user", "status")),
        ]

    def __str__(self):
        return f"{self.user_id} → {self.plan.code} ({self.status})"
