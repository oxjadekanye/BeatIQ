from django.contrib import admin

from .models import Album, Artist, Genre, Track


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_filter = ("artist",)
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_filter = ("explicit", "primary_artist")
    search_fields = ("title", "isrc", "slug")
    filter_horizontal = ("featured_artists", "genres")
    prepopulated_fields = {"slug": ("title",)}
