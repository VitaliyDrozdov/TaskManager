from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "assignees",
        "status",
        "planned_effort",
        "time_fact",
        "completed_at",
        "parent_task",
    )
    list_editable = (
        "description",
        "assignees",
        "status",
    )
    search_fields = (
        "name",
        "assignees",
    )
    list_filter = ("status",)
