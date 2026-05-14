from django.contrib import admin

from .models import AIMoodDiscoverySession, AIRecognitionPrepJob


@admin.register(AIMoodDiscoverySession)
class AIMoodDiscoverySessionAdmin(admin.ModelAdmin):
    list_display = ("user", "mood_label", "status", "created_at")


@admin.register(AIRecognitionPrepJob)
class AIRecognitionPrepJobAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "input_storage_object", "created_at")
