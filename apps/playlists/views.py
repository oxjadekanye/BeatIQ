from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.catalog.models import Track

from apps.core.drf_utils import is_schema_generation

from .models import AIPlaylistRecommendation, Playlist, PlaylistTrack
from .serializers import (
    AIPlaylistRecommendationSerializer,
    PlaylistSerializer,
    PlaylistWriteSerializer,
)


class PlaylistViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if is_schema_generation(self):
            return Playlist.objects.none()
        return Playlist.objects.filter(owner=self.request.user).prefetch_related(
            "items__track__primary_artist",
            "items__track__album",
            "items__track__genres",
        )

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return PlaylistWriteSerializer
        return PlaylistSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"], url_path="tracks")
    def add_track(self, request, pk=None):
        playlist = self.get_object()
        track_id = request.data.get("track_id")
        position = request.data.get("position", 0)
        track = get_object_or_404(Track, pk=track_id)
        PlaylistTrack.objects.update_or_create(
            playlist=playlist,
            track=track,
            defaults={"position": position},
        )
        return Response(PlaylistSerializer(playlist).data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[OpenApiParameter("track_id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
    )
    @action(detail=True, methods=["delete"], url_path=r"tracks/(?P<track_id>[^/.]+)")
    def remove_track(self, request, pk=None, track_id=None):
        playlist = self.get_object()
        PlaylistTrack.objects.filter(playlist=playlist, track_id=track_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AIPlaylistRecommendationViewSet(viewsets.ModelViewSet):
    serializer_class = AIPlaylistRecommendationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        if is_schema_generation(self):
            return AIPlaylistRecommendation.objects.none()
        return AIPlaylistRecommendation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        from apps.ai_services.services.recommendations import enqueue_playlist_recommendation_job

        rec = serializer.save(user=self.request.user, status=AIPlaylistRecommendation.Status.PENDING)
        enqueue_playlist_recommendation_job(rec)
