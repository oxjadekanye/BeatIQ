from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

from .models import Album, Artist, Genre, Track
from .serializers import (
    AlbumSerializer,
    ArtistSerializer,
    GenreSerializer,
    TrackDetailSerializer,
    TrackListSerializer,
)


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("name",)
    ordering_fields = ("name", "created_at")


class ArtistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("name",)
    ordering_fields = ("name", "created_at")


class AlbumViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Album.objects.select_related("artist").all()
    serializer_class = AlbumSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ("artist",)
    search_fields = ("title",)
    ordering_fields = ("release_date", "title")


class TrackViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Track.objects.select_related("primary_artist", "album")
        .prefetch_related("genres", "featured_artists")
        .all()
    )
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ("primary_artist", "album", "explicit")
    search_fields = ("title", "isrc")
    ordering_fields = ("title", "created_at")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TrackDetailSerializer
        return TrackListSerializer
