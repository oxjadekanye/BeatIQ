from rest_framework import serializers

from .models import AIMoodDiscoverySession, AIRecognitionPrepJob


class AIMoodDiscoverySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIMoodDiscoverySession
        fields = (
            "id",
            "mood_label",
            "mood_vector",
            "matched_track_ids",
            "status",
            "provider_job_id",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("matched_track_ids", "status", "provider_job_id", "created_at", "updated_at")


class AIRecognitionPrepJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIRecognitionPrepJob
        fields = (
            "id",
            "input_storage_object",
            "status",
            "fingerprint_handle",
            "notes",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("status", "fingerprint_handle", "created_at", "updated_at")
