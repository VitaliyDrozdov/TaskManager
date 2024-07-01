from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from tasks.forms import TaskForm
from tasks.models import Task


class TaskListView(generic.ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(parent_task__isnull=True)


class TaskDetailView(generic.DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"
    pk_url_kwarg = "task_id"


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:task_detail")


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    pk_url_kwarg = "task_id"

    def get_success_url(self) -> str:
        return reverse_lazy(
            "tasks:task_detail", kwargs={"task_id": self.object.id}
        )


class TaskDeleteView(generic.DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks:task_list")
    pk_url_kwarg = "task_id"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.subtasks.exists():
            return JsonResponse(
                {
                    "status": "error",
                    "errors": "Task with subtasks cannot be deleted",
                }
            )
        self.object.delete()
        return redirect(self.success_url)
