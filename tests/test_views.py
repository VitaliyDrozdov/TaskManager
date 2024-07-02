import pytest
from django.urls import reverse
from django.test import Client
from tasks.models import Task


@pytest.fixture
def client():
    return Client()


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
