from django.urls import path

from tasks.views import (
    TaskCreateView,
    TaskDeleteView,
    TaskDetailView,
    TaskListView,
    TaskUpdateView,
)

app_name = "tasks"

urlpatterns = [
    path("", TaskListView.as_view(), name="task_list"),
    path("<int:task_id>/", TaskDetailView.as_view(), name="task_detail"),
    path("create/", TaskCreateView.as_view(), name="task_create"),
    path("<int:task_id>/edit/", TaskUpdateView.as_view(), name="task_edit"),
    path(
        "<int:task_id>/delete/", TaskDeleteView.as_view(), name="task_delete"
    ),
]
