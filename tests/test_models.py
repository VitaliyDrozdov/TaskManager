import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from tasks.models import Task


@pytest.mark.django_db
def test_set_status_completed():
    task = Task.objects.create(
        name="Test Task", description="Test description", assignees="John Doe"
    )

    # Проверяем установку статуса 'Выполняется'
    task.set_status(Task.TaskStatus.IN_PROGRESS)
    assert task.status == Task.TaskStatus.IN_PROGRESS

    # subtask = Task.objects.create(
    #     name="Subtask",
    #     description="Subtask description",
    #     assignees="Jane Smith",
    #     parent_task=task,
    # )
    # with pytest.raises(ValidationError):
    #     task.set_status(Task.TaskStatus.COMPLETED)

    # subtask.set_status(Task.TaskStatus.COMPLETED)

    task.set_status(Task.TaskStatus.COMPLETED)
    assert task.status == Task.TaskStatus.COMPLETED
    assert task.completed_at is not None


@pytest.mark.django_db
def test_set_status_paused():
    task = Task.objects.create(
        name="Test Task", description="Test description", assignees="John Doe"
    )

    task.set_status(Task.TaskStatus.IN_PROGRESS)
    assert task.status == Task.TaskStatus.IN_PROGRESS
    task.set_status(Task.TaskStatus.PAUSED)
    assert task.status == Task.TaskStatus.PAUSED

    # with pytest.raises(ValidationError):
    #     task.set_status(Task.TaskStatus.PAUSED)


@pytest.mark.django_db
def test_task_calculate_efforts():
    task = Task.objects.create(
        name="Test Task", description="Test description", assignees="John Doe"
    )
    subtask1 = Task.objects.create(
        name="Subtask 1",
        description="Subtask 1 description",
        assignees="Jane Smith",
        parent_task=task,
    )
    subtask2 = Task.objects.create(
        name="Subtask 2",
        description="Subtask 2 description",
        assignees="Bob Brown",
        parent_task=task,
    )

    task.planned_effort = 10
    task.save()
    subtask1.planned_effort = 5
    subtask2.planned_effort = 3
    subtask1.save()
    subtask2.save()

    assert task.calculate_efforts() == 18


@pytest.mark.django_db
def test_task_calculate_time():
    task = Task.objects.create(
        name="Test Task", description="Test description", assignees="John Doe"
    )
    subtask1 = Task.objects.create(
        name="Subtask 1",
        description="Subtask 1 description",
        assignees="Jane Smith",
        parent_task=task,
    )
    subtask2 = Task.objects.create(
        name="Subtask 2",
        description="Subtask 2 description",
        assignees="Bob Brown",
        parent_task=task,
    )

    task.time_fact = 8
    task.save()
    subtask1.time_fact = 3
    subtask2.time_fact = 2
    subtask1.save()
    subtask2.save()
    assert task.calculate_time() == 13
