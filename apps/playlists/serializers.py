from rest_framework import serializers

from apps.catalog.serializers import TrackListSerializer

from .models import AIPlaylistRecommendation, Playlist, PlaylistTrack


class PlaylistTrackSerializer(serializers.ModelSerializer):
    track = TrackListSerializer(read_only=True)
    track_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = PlaylistTrack
        fields = ("id", "track", "track_id", "position")


class PlaylistSerializer(serializers.ModelSerializer):
    items = PlaylistTrackSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = (
            "id",
            "name",
            "description",
            "is_public",
            "mood_tags",
            "items",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "items", "created_at", "updated_at")


class PlaylistWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ("name", "description", "is_public", "mood_tags")


class AIPlaylistRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIPlaylistRecommendation
        fields = (
            "id",
            "playlist",
            "status",
            "seed_track_ids",
            "recommended_track_ids",
            "explanation",
            "provider_job_id",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("status", "recommended_track_ids", "explanation", "provider_job_id", "created_at", "updated_at")
