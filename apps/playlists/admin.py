from django.contrib import admin

from .models import AIPlaylistRecommendation, Playlist, PlaylistTrack


class PlaylistTrackInline(admin.TabularInline):
    model = PlaylistTrack
    extra = 0


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "is_public")
    inlines = (PlaylistTrackInline,)


@admin.register(AIPlaylistRecommendation)
class AIPlaylistRecommendationAdmin(admin.ModelAdmin):
    list_display = ("user", "playlist", "status", "created_at")
    list_filter = ("status",)
