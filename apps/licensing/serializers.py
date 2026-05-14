from rest_framework import serializers

from apps.catalog.serializers import TrackListSerializer

from .models import DownloadPermission, LegalSource, LicensedTrackSource, MusicLicense


class MusicLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicLicense
        fields = (
            "id",
            "code",
            "name",
            "summary",
            "external_reference",
            "is_active",
            "created_at",
            "updated_at",
        )


class LegalSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalSource
        fields = (
            "id",
            "name",
            "slug",
            "kind",
            "base_url",
            "is_verified_partner",
            "created_at",
            "updated_at",
        )


class DownloadPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownloadPermission
        fields = (
            "id",
            "allows_download",
            "valid_from",
            "valid_until",
            "max_bitrate_kbps",
            "requires_subscription_plan",
            "notes",
            "created_at",
            "updated_at",
        )


class LicensedTrackSourceSerializer(serializers.ModelSerializer):
    track = TrackListSerializer(read_only=True)
    legal_source = LegalSourceSerializer(read_only=True)
    license = MusicLicenseSerializer(read_only=True)
    download_permission = DownloadPermissionSerializer(read_only=True)

    class Meta:
        model = LicensedTrackSource
        fields = (
            "id",
            "track",
            "legal_source",
            "license",
            "partner_track_id",
            "canonical_reference_url",
            "is_active",
            "download_permission",
            "created_at",
            "updated_at",
        )
