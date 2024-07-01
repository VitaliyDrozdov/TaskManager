from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    class TaskStatus(models.TextChoices):
        ASSIGNED = "ASSIGNED", _("Назначана")
        IN_PROGRESS = "IN_PROGRESS", _("Выполняется")
        PAUSED = "PAUSED", _("Приостановлена")
        COMPLETED = "COMPLETED", _("Завершена")

    name = models.CharField("Название", max_length=50, unique=True)
    description = models.TextField("Описание")
    assignees = models.TextField("Исполнители")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Создано"
    )
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.ASSIGNED,
        verbose_name="Статус",
        db_index=True,
    )
    planned_effort = models.IntegerField(
        default=0, verbose_name="Плановая трудоемкость"
    )
    time_fact = models.IntegerField(
        default=0, verbose_name="Фактическое выполнение"
    )
    completed_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Дата заверщения"
    )
    parent_task = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="subtasks",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return self.name

    def calculate_efforts(self):
        subtasks = self.subtasks.all()
        return self.planned_effort + (
            sum(val.calculate_efforts() for val in subtasks)
        )

    def calculate_time(self):
        subtasks = self.subtasks.all()
        return sum(val.calculate_time() for val in subtasks) + self.time_fact

    def save(self, *args, **kwargs):
        self.check_status()
        self.calculate_efforts()
        self.calculate_time()
        if self.status == self.TaskStatus.COMPLETED:
            self.complete_tasks_subtasks()
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)

    def check_status(self):
        if self.status == self.TaskStatus.COMPLETED:
            # if (
            #     self.parent_task
            #     and self.parent_task.status != self.TaskStatus.COMPLETED
            # ):
            #     raise ValidationError(
            #         "Нельзя завершить задачу, если подзадачи не завершены."
            #     )
            for subtask in self.subtasks.all():
                if subtask.status != self.TaskStatus.COMPLETED:
                    raise ValidationError(
                        "Нельзя завершить задачу, если подзадачи не завершены."
                    )
        if self.pk:
            prev_status = Task.objects.get(pk=self.pk).status
            if (
                self.status == self.TaskStatus.COMPLETED
                or self.status == self.TaskStatus.PAUSED
            ) and prev_status != self.TaskStatus.IN_PROGRESS:
                raise ValidationError(
                    'Для данного действия необходим статус "В работе".'
                )

    def complete_tasks_subtasks(self):
        self.status = self.TaskStatus.COMPLETED
        for subtask in self.subtasks.all():
            subtask.complete_tasks_subtasks()
        self.save()
