from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from tasks.forms import TaskForm
from tasks.models import Task


class TaskListView(generic.ListView):
    model = Task
    template_name = "tasks/task_list.html"
    ordering = "created_at"
    paginate_by = 10
    context_object_name = "tasks"

    def get_queryset(self):
        tasks = Task.objects.filter(parent_task__isnull=True)
        for task in tasks:
            task.total_planned_effort = task.total_planned_effort
            task.total_time_fact = task.total_time_fact
        return tasks


class TaskDetailView(generic.DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"
    pk_url_kwarg = "task_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.object

        context["total_planned_effort"] = task.total_planned_effort
        context["total_time_fact"] = task.total_time_fact
        context["tasks"] = Task.objects.all()

        return context


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "tasks:task_detail", kwargs={"task_id": self.object.id}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = Task.objects.all()
        return context


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    pk_url_kwarg = "task_id"

    def form_valid(self, form):
        task = self.get_object()
        new_status = form.cleaned_data.get("status")
        try:
            task.set_status(new_status)
        except ValidationError as e:
            form.add_error("status", str(e))
            return self.form_invalid(form)
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self) -> str:
        return reverse_lazy(
            "tasks:task_detail", kwargs={"task_id": self.object.id}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = Task.objects.all()
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = Task.objects.all()
        return context


def redirect_to_tasks(request):
    return redirect("tasks:task_list")
