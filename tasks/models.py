from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Task(models.Model):
    class TaskStatus(models.TextChoices):
        ASSIGNED = "ASSIGNED", _("Назначана")
        IN_PROGRESS = "IN_PROGRESS", _("Выполняется")
        PASUSED = "PAUSED", _("Приостановлена")
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
        self.planned_effort = (
            sum(val.calculate_efforts() for val in subtasks)
            + self.planned_effort
        )
        return self.planned_effort

    def calculate_time(self):
        subtasks = self.subtasks.all()
        self.time_fact = (
            sum(val.calculate_time() for val in subtasks) + self.time_fact
        )
        return self.time_fact

    def save(self, *args, **kwargs):
        self.calculate_efforts()
        self.calculate_time()
        super().save(*args, **kwargs)
