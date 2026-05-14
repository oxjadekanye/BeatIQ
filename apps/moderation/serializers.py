from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from .models import ModerationAction, ModerationReport


class ModerationActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModerationAction
        fields = ("id", "moderator", "action_type", "note", "metadata", "created_at", "updated_at")
        read_only_fields = ("moderator", "created_at", "updated_at")


class ModerationReportSerializer(serializers.ModelSerializer):
    actions = ModerationActionSerializer(many=True, read_only=True)

    class Meta:
        model = ModerationReport
        fields = (
            "id",
            "reason_code",
            "description",
            "status",
            "subject_content_type",
            "subject_object_id",
            "actions",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("status", "actions", "created_at", "updated_at")


class ModerationReportCreateSerializer(serializers.ModelSerializer):
    subject_type = serializers.CharField(write_only=True)
    subject_id = serializers.CharField(write_only=True, max_length=64)

    class Meta:
        model = ModerationReport
        fields = ("reason_code", "description", "subject_type", "subject_id")

    def create(self, validated_data):
        from django.apps import apps

        model_label = validated_data.pop("subject_type")
        subject_id = validated_data.pop("subject_id")
        app_label, model_name = model_label.split(".", 1)
        model_cls = apps.get_model(app_label, model_name)
        subject = model_cls.objects.get(pk=subject_id)
        ct = ContentType.objects.get_for_model(subject.__class__)
        return ModerationReport.objects.create(
            reporter=self.context["request"].user,
            subject_content_type=ct,
            subject_object_id=str(subject.pk),
            **validated_data,
        )
