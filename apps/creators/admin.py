from django.contrib import admin

from .models import CreatorProfile, CreatorUploadAsset, CreatorUploadBatch


class CreatorUploadAssetInline(admin.TabularInline):
    model = CreatorUploadAsset
    extra = 0


@admin.register(CreatorProfile)
class CreatorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "display_name", "verification_status")


@admin.register(CreatorUploadBatch)
class CreatorUploadBatchAdmin(admin.ModelAdmin):
    inlines = (CreatorUploadAssetInline,)
