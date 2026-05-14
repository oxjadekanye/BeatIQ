from django.contrib import admin

from .models import ManagedStorageObject, StorageProvider


@admin.register(StorageProvider)
class StorageProviderAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "backend_kind", "is_active")


@admin.register(ManagedStorageObject)
class ManagedStorageObjectAdmin(admin.ModelAdmin):
    list_display = ("object_key", "provider", "owner", "size_bytes", "created_at")
    search_fields = ("object_key", "checksum_sha256")
