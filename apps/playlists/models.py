from django.conf import settings
from django.db import models

from apps.catalog.models import Track
from apps.core.models import UUIDTimeStampedModel


class Playlist(UUIDTimeStampedModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="playlists",
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False, db_index=True)
    mood_tags = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = "playlists_playlist"
        ordering = ("name",)

    def __str__(self):
        return self.name


class PlaylistTrack(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name="items")
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="playlist_items")
    position = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "playlists_playlist_track"
        ordering = ("position",)
        unique_together = ("playlist", "track")


class AIPlaylistRecommendation(UUIDTimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        READY = "ready", "Ready"
        FAILED = "failed", "Failed"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ai_playlist_recommendations",
    )
    playlist = models.ForeignKey(
        Playlist,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ai_recommendations",
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    seed_track_ids = models.JSONField(default=list, blank=True)
    recommended_track_ids = models.JSONField(default=list, blank=True)
    explanation = models.TextField(blank=True)
    provider_job_id = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "playlists_ai_playlist_recommendation"
