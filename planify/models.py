from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Task(models.Model):
    class Status(models.TextChoices):
        DRAFT = ('draft', 'Черновик')
        READY = ('ready', 'Готова к выполнению')
        IN_PROGRESS = ('in_progress', 'В процессе')
        COMPLETED = ('completed', 'Выполнена')
        CANCELED = ('canceled', 'Отменена')

    class Priority(models.TextChoices):
        NONE = ('none', 'Без приоритета')
        LOW = ('low', 'Низкий')
        MEDIUM = ('medium', 'Средний')
        HIGH = ('high', 'Высокий')

    PRIORITY_COLORS = {
        Priority.NONE: 'gray',
        Priority.LOW: 'green',
        Priority.MEDIUM: 'yellow',
        Priority.HIGH: 'red'
    }

    task_title = models.CharField(
        verbose_name='Название задачи',
        max_length=100,
        help_text="Краткое описание задачи",
    )
    task_description = models.CharField(
        verbose_name='Описание задачи',
        max_length=1000,
        blank=True,
        help_text="Подробное описание задачи",
    )
    task_status = models.CharField(
        verbose_name='Статус задачи',
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    task_priority = models.CharField(
        verbose_name='Приоритет задачи',
        max_length=20,
        choices=Priority.choices,
        default=Priority.NONE,
    )
    task_owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='Владелец',
    )
    task_due_date = models.DateTimeField(
        verbose_name='Срок выполнения задачи',
        null=True,
        blank=True,
    )
    task_created_at = models.DateTimeField(
        verbose_name='Дата создания задачи',
        auto_now_add=True,
    )
    task_updated_at = models.DateTimeField(
        verbose_name='Дата обновления задачи',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-task_due_date', '-task_priority']

    def __str__(self):
        return self.task_title

    @property
    def priority_color(self):
        return self.PRIORITY_COLORS.get(self.task_priority, 'gray')
