from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from tasks.forms import TaskForm
from tasks.models import Task


def task_list(request):
    tasks = Task.objects.filter(parent_task__isnull=True)
    return render(request, "tasks/task_list.html", {"tasks": tasks})


def task_detail(request, task_id):
    task = get_object_or_404(Task, task_id=task_id)
    return render(request, "tasks/task_detail.html", {"task": task})


def task_create(request):
    form = TaskForm(request.POST, instance=Task)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": "succes"})
    return JsonResponse({"status": "error", "errors": form.errors})


def task_edit(request, task_id):
    task = get_object_or_404(Task, task_id=task_id)
    form = TaskForm(request.POST, instance=Task)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": "succes", "task": task})
    return JsonResponse({"status": "error", "errors": form.errors})
