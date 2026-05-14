from django.contrib import admin

from .models import SocialLinkMetadata


@admin.register(SocialLinkMetadata)
class SocialLinkMetadataAdmin(admin.ModelAdmin):
    list_display = ("raw_url", "platform", "detected_title", "detected_artist", "confidence")
