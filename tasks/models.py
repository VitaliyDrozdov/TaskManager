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

    total_planned_effort = models.IntegerField(
        default=0, verbose_name="Общая плановая трудоемкость"
    )
    total_time_fact = models.IntegerField(
        default=0, verbose_name="Общее фактическое выполнение"
    )

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return self.name

    def calculate_efforts(self):
        subtasks = self.subtasks.all()
        if not subtasks:
            return self.planned_effort
        else:
            return self.planned_effort + (
                sum(val.calculate_efforts() for val in subtasks)
            )

    def calculate_time(self):
        subtasks = self.subtasks.all()
        if not subtasks:
            return self.time_fact
        else:
            return (
                sum(val.calculate_time() for val in subtasks) + self.time_fact
            )

    def set_status(self, new_status):
        current_status = self.status
        if new_status == current_status:
            return
        if new_status == Task.TaskStatus.COMPLETED:
            if current_status != Task.TaskStatus.IN_PROGRESS:
                raise ValidationError(
                    "Завершение задачи возможно только"
                    " из статуса 'Выполняется'."
                )
            for subtask in self.subtasks.all():
                subtask.set_status(new_status)
            if all(
                subtask.status == Task.TaskStatus.COMPLETED
                for subtask in self.subtasks.all()
            ):
                self.status = new_status
                self.completed_at = timezone.now()
                self.save(update_fields=["status", "completed_at"])
            else:
                raise ValidationError("Не все подзадачи могут быть завершены")

        elif new_status == Task.TaskStatus.PAUSED:
            if current_status != Task.TaskStatus.IN_PROGRESS:
                raise ValidationError(
                    "Приостановка задачи возможна только "
                    " из статуса 'Выполняется'."
                )
            self.status = new_status
            self.save(update_fields=["status"])

        else:
            self.status = new_status
            self.save(update_fields=["status"])

    def clean(self):
        super().clean()
        if self.parent_task == self:
            raise ValidationError(
                "Задача не может быть подзадачей для самой себя."
            )

    def save(self, *args, **kwargs):
        update_fields = kwargs.get("update_fields", None)
        if not self.pk:
            self.status = self.TaskStatus.ASSIGNED
            super().save(*args, **kwargs)
        if update_fields is None or "planned_effort" in update_fields:
            self.total_planned_effort = self.calculate_efforts()

        if update_fields is None or "time_fact" in update_fields:
            self.total_time_fact = self.calculate_time()
        super().save(update_fields=update_fields)
