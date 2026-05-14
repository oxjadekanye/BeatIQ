from rest_framework import serializers

from .models import ManagedStorageObject, StorageProvider


class StorageProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageProvider
        fields = ("id", "code", "name", "backend_kind", "is_active", "created_at", "updated_at")


class ManagedStorageObjectSerializer(serializers.ModelSerializer):
    provider = StorageProviderSerializer(read_only=True)

    class Meta:
        model = ManagedStorageObject
        fields = (
            "id",
            "provider",
            "object_key",
            "bucket_name",
            "media_type",
            "size_bytes",
            "checksum_sha256",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields
