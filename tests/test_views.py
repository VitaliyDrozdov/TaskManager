import pytest
from django.urls import reverse
from tasks.models import Task


@pytest.mark.django_db
def test_task_list_view(client):
    url = reverse("tasks:task_list")
    response = client.get(url)
    assert response.status_code == 200
    assert "tasks/task_list.html" in [
        template.name for template in response.templates
    ]


@pytest.mark.django_db
def test_task_list_view_with_tasks(client):
    task1 = Task.objects.create(
        name="Task 1", description="Description 1", assignees="User1"
    )
    task2 = Task.objects.create(
        name="Task 2", description="Description 2", assignees="User2"
    )

    url = reverse("tasks:task_list")
    response = client.get(url)

    assert response.status_code == 200
    assert task1 in response.context["tasks"]
    assert task2 in response.context["tasks"]


@pytest.mark.django_db
def test_task_detail_view(client):
    task = Task.objects.create(
        name="Task 1", description="Description 1", assignees="User1"
    )
    url = reverse("tasks:task_detail", kwargs={"task_id": task.id})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["task"] == task
    assert "tasks/task_detail.html" in [
        template.name for template in response.templates
    ]


@pytest.mark.django_db
def test_task_detail_view_not_found(client):
    url = reverse("tasks:task_detail", kwargs={"task_id": 999})
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_task_create_view(client):
    url = reverse("tasks:task_create")
    response = client.get(url)
    assert response.status_code == 200
    assert "tasks/task_form.html" in [
        template.name for template in response.templates
    ]


@pytest.mark.django_db
def test_task_update_view(client):
    task = Task.objects.create(
        name="Task 1", description="Description 1", assignees="User1"
    )
    url = reverse("tasks:task_edit", kwargs={"task_id": task.id})
    response = client.get(url)
    assert response.status_code == 200
    assert "tasks/task_form.html" in [
        template.name for template in response.templates
    ]


@pytest.mark.django_db
def test_task_delete_view(client):
    task = Task.objects.create(
        name="Task 1", description="Description 1", assignees="User1"
    )
    url = reverse("tasks:task_delete", kwargs={"task_id": task.id})
    response = client.get(url)
    assert response.status_code == 200
    assert "tasks/task_confirm_delete.html" in [
        template.name for template in response.templates
    ]


@pytest.mark.django_db
def test_task_delete_post(client):
    task = Task.objects.create(
        name="Task 1", description="Description 1", assignees="User1"
    )
    url = reverse("tasks:task_delete", kwargs={"task_id": task.id})
    response = client.post(url)
    assert response.status_code == 302
    assert not Task.objects.filter(id=task.id).exists()
