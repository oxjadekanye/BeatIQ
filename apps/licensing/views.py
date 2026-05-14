from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.catalog.models import Track

from .models import LegalSource, LicensedTrackSource, MusicLicense
from .serializers import LegalSourceSerializer, LicensedTrackSourceSerializer, MusicLicenseSerializer
from .services.download_eligibility import summarize_track_download_policy


class MusicLicenseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MusicLicense.objects.filter(is_active=True)
    serializer_class = MusicLicenseSerializer
    permission_classes = (permissions.AllowAny,)


class LegalSourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LegalSource.objects.filter(is_verified_partner=True)
    serializer_class = LegalSourceSerializer
    permission_classes = (permissions.AllowAny,)


class TrackSourcesView(APIView):
    """List legal source mappings for a track (read-only)."""

    permission_classes = (permissions.AllowAny,)

    @extend_schema(
        parameters=[OpenApiParameter("track_id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
        responses={200: LicensedTrackSourceSerializer(many=True)},
    )
    def get(self, request, track_id):
        track = get_object_or_404(Track, pk=track_id)
        qs = (
            LicensedTrackSource.objects.filter(track=track, is_active=True)
            .select_related(
                "legal_source",
                "license",
                "download_permission",
                "track",
                "track__album",
                "track__primary_artist",
            )
        )
        return Response(LicensedTrackSourceSerializer(qs, many=True).data)


class TrackDownloadEligibilityView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(
        parameters=[OpenApiParameter("track_id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request, track_id):
        track = get_object_or_404(Track, pk=track_id)
        return Response(summarize_track_download_policy(request.user, track))
