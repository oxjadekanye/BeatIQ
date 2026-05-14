from django.contrib import admin

from .models import DownloadPermission, LegalSource, LicensedTrackSource, MusicLicense


class DownloadPermissionInline(admin.StackedInline):
    model = DownloadPermission
    extra = 0


@admin.register(MusicLicense)
class MusicLicenseAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("code", "name")


@admin.register(LegalSource)
class LegalSourceAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "kind", "is_verified_partner")
    list_filter = ("kind", "is_verified_partner")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(LicensedTrackSource)
class LicensedTrackSourceAdmin(admin.ModelAdmin):
    list_display = ("track", "legal_source", "license", "is_active")
    list_filter = ("is_active", "legal_source")
    inlines = (DownloadPermissionInline,)


@admin.register(DownloadPermission)
class DownloadPermissionAdmin(admin.ModelAdmin):
    list_display = (
        "licensed_track_source",
        "allows_download",
        "valid_from",
        "valid_until",
        "requires_subscription_plan",
    )
    list_filter = ("allows_download",)
