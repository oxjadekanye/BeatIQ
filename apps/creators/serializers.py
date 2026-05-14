from rest_framework import serializers

from apps.storage_integration.serializers import ManagedStorageObjectSerializer

from .models import CreatorProfile, CreatorUploadAsset, CreatorUploadBatch


class CreatorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreatorProfile
        fields = (
            "id",
            "display_name",
            "verification_status",
            "rights_attestation",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("verification_status", "created_at", "updated_at")


class CreatorUploadAssetSerializer(serializers.ModelSerializer):
    storage_object = ManagedStorageObjectSerializer(read_only=True)

    class Meta:
        model = CreatorUploadAsset
        fields = (
            "id",
            "title",
            "storage_object",
            "review_status",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("storage_object", "review_status", "created_at", "updated_at")


class CreatorUploadBatchSerializer(serializers.ModelSerializer):
    assets = CreatorUploadAssetSerializer(many=True, read_only=True)

    class Meta:
        model = CreatorUploadBatch
        fields = ("id", "title", "assets", "created_at", "updated_at")
