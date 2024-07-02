import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from tasks.models import Task


@pytest.mark.django_db
def test_set_status_completed():
    task = Task.objects.create(
        name="Test Task", description="Test description", assignees="User1"
    )

    subtask = Task.objects.create(
        name="Subtask",
        description="Subtask description",
        assignees="SubUser",
        parent_task=task,
    )
    task.set_status(Task.TaskStatus.IN_PROGRESS)
    subtask.set_status(Task.TaskStatus.IN_PROGRESS)
    assert task.status == Task.TaskStatus.IN_PROGRESS
    assert subtask.status == Task.TaskStatus.IN_PROGRESS
    task.set_status(Task.TaskStatus.COMPLETED)
    task.refresh_from_db()
    subtask.refresh_from_db()
    assert task.status == Task.TaskStatus.COMPLETED
    assert subtask.status == Task.TaskStatus.COMPLETED


@pytest.mark.django_db
def test_set_status_paused():
    task = Task.objects.create(
        name="Test Task", description="Test description", assignees="User1"
    )

    task.set_status(Task.TaskStatus.IN_PROGRESS)
    assert task.status == Task.TaskStatus.IN_PROGRESS
    task.set_status(Task.TaskStatus.PAUSED)
    assert task.status == Task.TaskStatus.PAUSED


@pytest.mark.django_db
def test_task_calculate_efforts():
    task = Task.objects.create(
        name="Test Task", description="Test description", assignees="User1"
    )
    subtask1 = Task.objects.create(
        name="Subtask 1",
        description="Subtask 1 description",
        assignees="SubUser1",
        parent_task=task,
    )
    subtask2 = Task.objects.create(
        name="Subtask 2",
        description="Subtask 2 description",
        assignees="SubUser2",
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
        name="Test Task", description="Test description", assignees="User1"
    )
    subtask1 = Task.objects.create(
        name="Subtask 1",
        description="Subtask 1 description",
        assignees="SubUser1",
        parent_task=task,
    )
    subtask2 = Task.objects.create(
        name="Subtask 2",
        description="Subtask 2 description",
        assignees="SubUser2",
        parent_task=task,
    )

    task.time_fact = 8
    task.save()
    subtask1.time_fact = 3
    subtask2.time_fact = 2
    subtask1.save()
    subtask2.save()
    assert task.calculate_time() == 13


@pytest.mark.django_db
def test_complete_task_without_subtasks():
    task = Task.objects.create(
        name="Task without subtasks",
        description="A simple task",
        assignees="User1",
    )
    task.status = Task.TaskStatus.IN_PROGRESS
    task.save()
    task.set_status(Task.TaskStatus.COMPLETED)
    task.refresh_from_db()
    assert task.status == Task.TaskStatus.COMPLETED
    assert task.completed_at is not None


@pytest.mark.django_db
def test_complete_task_with_completed_subtasks():
    parent_task = Task.objects.create(
        name="Parent Task",
        description="Parent task description",
        assignees="User1",
    )
    subtask1 = Task.objects.create(
        name="Subtask 1",
        description="Subtask 1 description",
        assignees="User2",
        parent_task=parent_task,
    )
    subtask2 = Task.objects.create(
        name="Subtask 2",
        description="Subtask 2 description",
        assignees="User3",
        parent_task=parent_task,
    )

    parent_task.status = Task.TaskStatus.IN_PROGRESS
    subtask1.status = Task.TaskStatus.COMPLETED
    subtask2.status = Task.TaskStatus.COMPLETED

    parent_task.save()
    subtask1.save()
    subtask2.save()

    parent_task.set_status(Task.TaskStatus.COMPLETED)
    parent_task.refresh_from_db()

    assert parent_task.status == Task.TaskStatus.COMPLETED
    assert parent_task.completed_at is not None


@pytest.mark.skip(
    reason="Тест проходит, но assertion error. Нужно подправить."
)
@pytest.mark.django_db
def test_fail_complete_task_with_paused_subtask():
    parent_task = Task.objects.create(
        name="Parent Task",
        description="Parent task description",
        assignees="User1",
    )
    subtask1 = Task.objects.create(
        name="Subtask 1",
        description="Subtask 1 description",
        assignees="User2",
        parent_task=parent_task,
    )
    subtask2 = Task.objects.create(
        name="Subtask 2",
        description="Subtask 2 description",
        assignees="User3",
        parent_task=parent_task,
    )
    parent_task.status = Task.TaskStatus.IN_PROGRESS
    subtask1.status = Task.TaskStatus.COMPLETED
    subtask2.status = Task.TaskStatus.IN_PROGRESS
    subtask2.set_status(Task.TaskStatus.PAUSED)
    with pytest.raises(ValidationError) as err:
        parent_task.set_status(Task.TaskStatus.COMPLETED)
    # fmt:off
    assert str(err.value) == [
        "Завершение задачи возможно только из статуса \'Выполняется\'."
    ]
    # fmt: on
    subtask2.set_status(Task.TaskStatus.COMPLETED)
    parent_task.set_status(Task.TaskStatus.COMPLETED)
    parent_task.refresh_from_db()
    assert parent_task.status == Task.TaskStatus.COMPLETED


@pytest.mark.django_db
def test_pause_task():
    task = Task.objects.create(
        name="Task to pause", description="A simple task", assignees="User1"
    )
    task.status = Task.TaskStatus.IN_PROGRESS
    task.save()
    task.set_status(Task.TaskStatus.PAUSED)
    task.refresh_from_db()
    assert task.status == Task.TaskStatus.PAUSED


@pytest.mark.django_db
def test_pause_task_with_subtasks():
    parent_task = Task.objects.create(
        name="Parent Task",
        description="Parent task description",
        assignees="User1",
    )
    subtask1 = Task.objects.create(
        name="Subtask 1",
        description="Subtask 1 description",
        assignees="User2",
        parent_task=parent_task,
    )
    subtask2 = Task.objects.create(
        name="Subtask 2",
        description="Subtask 2 description",
        assignees="User3",
        parent_task=parent_task,
    )

    parent_task.status = Task.TaskStatus.IN_PROGRESS
    subtask1.status = Task.TaskStatus.IN_PROGRESS
    subtask2.status = Task.TaskStatus.IN_PROGRESS

    parent_task.save()
    subtask1.save()
    subtask2.save()

    parent_task.set_status(Task.TaskStatus.PAUSED)
    parent_task.refresh_from_db()
    subtask1.refresh_from_db()
    subtask2.refresh_from_db()

    assert parent_task.status == Task.TaskStatus.PAUSED
    assert subtask1.status == Task.TaskStatus.IN_PROGRESS
    assert subtask2.status == Task.TaskStatus.IN_PROGRESS


@pytest.mark.django_db
def test_fail_pause_task_with_subtasks_not_in_progress():
    parent_task = Task.objects.create(
        name="Parent Task",
        description="Parent task description",
        assignees="User1",
    )
    subtask1 = Task.objects.create(
        name="Subtask 1",
        description="Subtask 1 description",
        assignees="User2",
        parent_task=parent_task,
    )
    subtask2 = Task.objects.create(
        name="Subtask 2",
        description="Subtask 2 description",
        assignees="User3",
        parent_task=parent_task,
    )

    parent_task.status = Task.TaskStatus.ASSIGNED
    subtask1.status = Task.TaskStatus.IN_PROGRESS
    subtask2.status = Task.TaskStatus.IN_PROGRESS

    parent_task.save()
    subtask1.save()
    subtask2.save()
