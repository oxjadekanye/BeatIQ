from rest_framework import serializers

from apps.catalog.serializers import TrackListSerializer

from .models import SocialLinkMetadata


class SocialLinkMetadataSerializer(serializers.ModelSerializer):
    resolved_track = TrackListSerializer(read_only=True)

    class Meta:
        model = SocialLinkMetadata
        fields = (
            "id",
            "raw_url",
            "normalized_url",
            "platform",
            "detected_title",
            "detected_artist",
            "confidence",
            "resolved_track",
            "raw_metadata",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "normalized_url",
            "platform",
            "detected_title",
            "detected_artist",
            "confidence",
            "resolved_track",
            "raw_metadata",
            "created_at",
            "updated_at",
        )


class SocialLinkResolveRequestSerializer(serializers.Serializer):
    url = serializers.URLField(max_length=800)
