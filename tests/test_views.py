import pytest
from django.urls import reverse
from django.test import Client
from tasks.models import Task


# @pytest.fixture
# def client():
#     return Client()


# @pytest.mark.django_db
# def test_task_create_view(client):
#     url = reverse("tasks:task_create")

#     data = {
#         "name": "Test Task",
#         "description": "Test description",
#         "assignees": "John Doe",
#         "status": Task.TaskStatus.ASSIGNED,
#     }

#     response = client.post(url, data, follow=True)

#     assert response.status_code == 200  # Проверяем успешное перенаправление
#     assert response.redirect_chain  # Проверяем, что было перенаправление
#     assert (
#         response.redirect_chain[0][1] == 200
#     )  # Убеждаемся, что статус код перенаправления был 302


# @pytest.mark.django_db
# def test_task_update_view(client):
#     task = Task.objects.create(
#         name="Test Task", description="Test description", assignees="John Doe"
#     )
#     url = reverse("tasks:task_edit", kwargs={"task_id": task.id})

#     data = {
#         "name": "Updated Task",
#         "description": "Updated description",
#         "assignees": "Jane Smith",
#         "status": Task.TaskStatus.IN_PROGRESS,
#     }

#     response = client.post(url, data, follow=True)

#     assert response.status_code == 200  # Проверяем успешное перенаправление
#     assert response.redirect_chain  # Проверяем, что было перенаправление
#     assert (
#         response.redirect_chain[0][1] == 200
#     )  # Убеждаемся, что статус код перенаправления был 302


# @pytest.mark.django_db
# def test_task_delete_view(client):
#     task = Task.objects.create(
#         name="Test Task", description="Test description", assignees="John Doe"
#     )
#     url = reverse("tasks:task_delete", kwargs={"task_id": task.id})

#     response = client.post(url, follow=True)

#     assert response.status_code == 200  # Проверяем успешное перенаправление
#     assert response.redirect_chain  # Проверяем, что было перенаправление
#     assert (
#         response.redirect_chain[0][1] == 200
#     )  # Убеждаемся, что статус код перенаправления был 302


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
def test_task_create_post(client):
    data = {
        "name": "New Task",
        "description": "New Description",
        "assignees": "User1, User2",
    }
    url = reverse("tasks:task_create")
    response = client.post(url, data)
    assert response.status_code == 302
    assert Task.objects.filter(name="New Task").exists()


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
def test_task_update_post(client):
    task = Task.objects.create(
        name="Task 1", description="Description 1", assignees="User1"
    )
    url = reverse("tasks:task_edit", kwargs={"task_id": task.id})
    data = {
        "name": "Updated Task",
        "description": "Updated Description",
        "assignees": "User1, User2",
    }
    response = client.post(url, data)
    assert response.status_code == 302
    task.refresh_from_db()
    assert task.name == "Updated Task"


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
    assert response.status_code == 302  # Redirects on successful deletion
    assert not Task.objects.filter(id=task.id).exists()
