import pytest
from django.core.exceptions import ValidationError

from tasks.models import Task


@pytest.mark.django_db
def test_task_create():
    task = Task.objects.create(
        name="Test Task",
        description="test description",
        assignees="User1, User2",
        planned_effort=5,
        time_fact=2,
        status=Task.TaskStatus.ASSIGNED,
    )
    assert task.pk is not None
    assert task.name == "Test Task"


# @pytest.mark.django_db
# def test_task_status():
#     task = Task.objects.create(
#         name="Test Task",
#         description="test description",
#         assignees="User1, User2",
#         planned_effort=5,
#         time_fact=2,
#         status=Task.TaskStatus.IN_PROGRESS,
#     )
#     task.status = Task.TaskStatus.COMPLETED
#     with pytest.raises(ValidationError):
#         task.save()


@pytest.mark.django_db
def test_complete_task_without_subtasks():
    task = Task.objects.create(
        name="Test Task",
        description="Test description",
        assignees="User1, User2",
        planned_effort=5,
        time_fact=2,
        status=Task.TaskStatus.IN_PROGRESS,
    )
    task.status = Task.TaskStatus.COMPLETED
    task.save()
    assert task.status == Task.TaskStatus.COMPLETED
    assert task.completed_at is not None


@pytest.mark.django_db
def test_complete_task_with_incomplete_subtasks():
    task = Task.objects.create(
        name="Parent Task",
        description="Parent task description",
        assignees="User1, User2",
        planned_effort=10,
        time_fact=5,
        status=Task.TaskStatus.IN_PROGRESS,
    )
    subtask1 = Task.objects.create(
        name="Subtask 1",
        description="Subtask 1 description",
        assignees="User3",
        planned_effort=3,
        time_fact=2,
        status=Task.TaskStatus.IN_PROGRESS,
        parent_task=task,
    )
    subtask2 = Task.objects.create(
        name="Subtask 2",
        description="Subtask 2 description",
        assignees="User4",
        planned_effort=2,
        time_fact=1,
        status=Task.TaskStatus.IN_PROGRESS,
        parent_task=task,
    )
    task.status = Task.TaskStatus.COMPLETED
    with pytest.raises(ValidationError):
        task.save()


@pytest.mark.django_db
def test_complete_task_with_complete_subtasks():
    task = Task.objects.create(
        name="Parent Task",
        description="Parent task description",
        assignees="User1, User2",
        planned_effort=10,
        time_fact=5,
        status=Task.TaskStatus.IN_PROGRESS,
    )
    subtask1 = Task.objects.create(
        name="Subtask 1",
        description="Subtask 1 description",
        assignees="User3",
        planned_effort=3,
        time_fact=3,
        status=Task.TaskStatus.COMPLETED,
        parent_task=task,
    )
    subtask2 = Task.objects.create(
        name="Subtask 2",
        description="Subtask 2 description",
        assignees="User4",
        planned_effort=2,
        time_fact=2,
        status=Task.TaskStatus.COMPLETED,
        parent_task=task,
    )
    task.status = Task.TaskStatus.COMPLETED
    task.save()
    assert task.status == Task.TaskStatus.COMPLETED
    assert task.completed_at is not None


@pytest.mark.django_db
def test_invalid_status():
    task = Task.objects.create(
        name="Test Task",
        description="Test description",
        assignees="User1, User2",
        planned_effort=5,
        time_fact=2,
        status=Task.TaskStatus.ASSIGNED,
    )
    task.status = Task.TaskStatus.COMPLETED
    with pytest.raises(ValidationError):
        task.save()


@pytest.mark.django_db
def test_invalid_complete_status():
    task = Task.objects.create(
        name="Parent Task",
        description="Parent task description",
        assignees="User1, User2",
        planned_effort=10,
        time_fact=5,
        status=Task.TaskStatus.IN_PROGRESS,
    )
    subtask1 = Task.objects.create(
        name="Subtask 1",
        description="Subtask 1 description",
        assignees="User3",
        planned_effort=3,
        time_fact=3,
        status=Task.TaskStatus.COMPLETED,
        parent_task=task,
    )
    subtask2 = Task.objects.create(
        name="Subtask 2",
        description="Subtask 2 description",
        assignees="User4",
        planned_effort=2,
        time_fact=2,
        status=Task.TaskStatus.IN_PROGRESS,
        parent_task=task,
    )
    task.status = Task.TaskStatus.COMPLETED
    with pytest.raises(ValidationError):
        task.save()


@pytest.mark.django_db
def test_parent_task_completion_affects_subtasks():
    task = Task.objects.create(
        name="Parent Task",
        description="Parent task description",
        assignees="User1, User2",
        planned_effort=10,
        time_fact=5,
        status=Task.TaskStatus.IN_PROGRESS,
    )
    subtask1 = Task.objects.create(
        name="Subtask 1",
        description="Subtask 1 description",
        assignees="User3",
        planned_effort=3,
        time_fact=3,
        status=Task.TaskStatus.IN_PROGRESS,
        parent_task=task,
    )
    subtask2 = Task.objects.create(
        name="Subtask 2",
        description="Subtask 2 description",
        assignees="User4",
        planned_effort=2,
        time_fact=2,
        status=Task.TaskStatus.IN_PROGRESS,
        parent_task=task,
    )

    task.status = Task.TaskStatus.COMPLETED
    task.save()
    assert task.status == Task.TaskStatus.COMPLETED
    assert task.completed_at is not None
    subtask1.refresh_from_db()
    subtask2.refresh_from_db()
    assert subtask1.status == Task.TaskStatus.COMPLETED
    assert subtask2.status == Task.TaskStatus.COMPLETED
