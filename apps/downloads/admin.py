from django.contrib import admin

from .models import ComplianceAuditLog, DownloadAuditLog, OfflineLibraryItem, SavedDownload


@admin.register(SavedDownload)
class SavedDownloadAdmin(admin.ModelAdmin):
    list_display = ("user", "track", "licensed_track_source", "completed_at", "created_at")
    list_filter = ("completed_at",)


@admin.register(DownloadAuditLog)
class DownloadAuditLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "user", "track", "action", "success", "reason_code")
    list_filter = ("action", "success")


@admin.register(OfflineLibraryItem)
class OfflineLibraryItemAdmin(admin.ModelAdmin):
    list_display = ("user", "track", "device_id", "removed_at")


@admin.register(ComplianceAuditLog)
class ComplianceAuditLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "user", "event_type")
