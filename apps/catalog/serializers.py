from rest_framework import serializers

from .models import Album, Artist, Genre, Track


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name", "slug", "created_at", "updated_at")


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = (
            "id",
            "name",
            "slug",
            "bio",
            "image_url",
            "official_website",
            "created_at",
            "updated_at",
        )


class AlbumSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)

    class Meta:
        model = Album
        fields = (
            "id",
            "title",
            "slug",
            "artist",
            "release_date",
            "cover_image_url",
            "label",
            "created_at",
            "updated_at",
        )


class TrackListSerializer(serializers.ModelSerializer):
    primary_artist = ArtistSerializer(read_only=True)

    class Meta:
        model = Track
        fields = (
            "id",
            "title",
            "slug",
            "album",
            "primary_artist",
            "duration_ms",
            "isrc",
            "explicit",
            "preview_stream_url",
            "created_at",
            "updated_at",
        )


class TrackDetailSerializer(TrackListSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    featured_artists = ArtistSerializer(many=True, read_only=True)

    class Meta(TrackListSerializer.Meta):
        fields = TrackListSerializer.Meta.fields + ("genres", "featured_artists")
