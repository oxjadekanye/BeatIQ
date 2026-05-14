from django.contrib import admin

from .models import ModerationAction, ModerationReport


class ModerationActionInline(admin.TabularInline):
    model = ModerationAction
    extra = 0


@admin.register(ModerationReport)
class ModerationReportAdmin(admin.ModelAdmin):
    list_display = ("id", "reason_code", "status", "reporter", "created_at")
    list_filter = ("status", "reason_code")
    inlines = (ModerationActionInline,)


@admin.register(ModerationAction)
class ModerationActionAdmin(admin.ModelAdmin):
    list_display = ("report", "moderator", "action_type", "created_at")
