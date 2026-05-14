from rest_framework import serializers

from .models import Plan, Subscription


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = (
            "id",
            "code",
            "name",
            "description",
            "tier_order",
            "price_monthly_cents",
            "is_public",
            "created_at",
            "updated_at",
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = (
            "id",
            "plan",
            "status",
            "current_period_start",
            "current_period_end",
            "cancel_at_period_end",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields
