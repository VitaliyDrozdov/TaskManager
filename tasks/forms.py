from django import forms

from tasks.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            "name",
            "description",
            "assignees",
            "status",
            "planned_effort",
            "time_fact",
            "completed_at",
            "parent_task",
        )

        widgets = {
            "completed_at": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%d.%m.%Y %H:%M"
            )
        }
