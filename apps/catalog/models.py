from django.db import models

from apps.core.models import UUIDTimeStampedModel


class Genre(UUIDTimeStampedModel):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=140, unique=True)

    class Meta:
        db_table = "catalog_genre"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Artist(UUIDTimeStampedModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True)
    bio = models.TextField(blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    official_website = models.URLField(max_length=500, blank=True)

    class Meta:
        db_table = "catalog_artist"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Album(UUIDTimeStampedModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="albums")
    release_date = models.DateField(null=True, blank=True)
    cover_image_url = models.URLField(max_length=500, blank=True)
    label = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "catalog_album"
        unique_together = ("artist", "slug")
        ordering = ("-release_date", "title")

    def __str__(self):
        return f"{self.title} — {self.artist}"


class Track(UUIDTimeStampedModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280)
    album = models.ForeignKey(
        Album,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tracks",
    )
    primary_artist = models.ForeignKey(
        Artist,
        on_delete=models.PROTECT,
        related_name="primary_tracks",
    )
    featured_artists = models.ManyToManyField(
        Artist,
        blank=True,
        related_name="featured_on_tracks",
    )
    genres = models.ManyToManyField(Genre, blank=True, related_name="tracks")
    duration_ms = models.PositiveIntegerField(default=0)
    isrc = models.CharField(max_length=15, blank=True, db_index=True)
    explicit = models.BooleanField(default=False)
    preview_stream_url = models.URLField(
        max_length=800,
        blank=True,
        help_text="Legal preview URL from a licensed partner only.",
    )

    class Meta:
        db_table = "catalog_track"
        unique_together = ("primary_artist", "slug")
        ordering = ("title",)

    def __str__(self):
        return f"{self.title} — {self.primary_artist}"
