import pytest
from django.urls import reverse

from tasks.models import Task


@pytest.mark.django_db
def test_task_list_view(client):
    Task.objects.create(
        name="Test Task",
        description="This is a test task",
        assignees="User1, User2",
        planned_effort=5,
        time_fact=2,
    )
    url = reverse("tasks:task_list")
    response = client.get(url)
    assert response.status_code == 200
    assert "Test Task" in response.content.decode()


@pytest.mark.django_db
def test_task_detail_view(client):
    task = Task.objects.create(
        name="Test Task",
        description="This is a test task",
        assignees="User1, User2",
        planned_effort=5,
        time_fact=2,
    )
    url = reverse("tasks:task_detail", args=[task.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert "Test Task" in response.content.decode()


@pytest.mark.django_db
def test_task_create_view(client):
    url = reverse("tasks:task_create")
    data = {
        "name": "New Task",
        "description": "This is a new task",
        "assignees": "User1, User2",
        "planned_effort": 5,
        "time_fact": 2,
        "status": Task.TaskStatus.ASSIGNED,
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Task.objects.filter(name="New Task").exists()


@pytest.mark.django_db
def test_task_update_view(client):
    task = Task.objects.create(
        name="Test Task",
        description="This is a test task",
        assignees="User1, User2",
        planned_effort=5,
        time_fact=2,
        status=Task.TaskStatus.ASSIGNED,
    )
    url = reverse("tasks:task_edit", args=[task.pk])
    data = {
        "name": "Updated Task",
        "description": "This is an updated task",
        "assignees": "User1, User2",
        "planned_effort": 6,
        "time_fact": 3,
        "status": Task.TaskStatus.IN_PROGRESS,
    }
    response = client.post(url, data)
    assert response.status_code == 302
    task.refresh_from_db()
    assert task.name == "Updated Task"


@pytest.mark.django_db
def test_task_delete_view(client):
    task = Task.objects.create(
        name="Test Task",
        description="This is a test task",
        assignees="User1, User2",
        planned_effort=5,
        time_fact=2,
    )
    url = reverse("tasks:task_delete", args=[task.pk])
    response = client.post(url)
    assert response.status_code == 302
    assert not Task.objects.filter(name="Test Task").exists()
