from rest_framework import serializers

from apps.catalog.serializers import TrackListSerializer
from apps.licensing.serializers import LicensedTrackSourceSerializer

from .models import OfflineLibraryItem, SavedDownload


class SavedDownloadSerializer(serializers.ModelSerializer):
    track = TrackListSerializer(read_only=True)
    licensed_track_source = LicensedTrackSourceSerializer(read_only=True)

    class Meta:
        model = SavedDownload
        fields = (
            "id",
            "track",
            "licensed_track_source",
            "permission_snapshot",
            "storage_object",
            "completed_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class OfflineLibraryItemSerializer(serializers.ModelSerializer):
    track = TrackListSerializer(read_only=True)

    class Meta:
        model = OfflineLibraryItem
        fields = (
            "id",
            "track",
            "device_id",
            "saved_download",
            "removed_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class OfflineLibraryUpsertSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineLibraryItem
        fields = ("track", "device_id", "saved_download")
