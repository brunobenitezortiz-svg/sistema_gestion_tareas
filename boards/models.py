from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Board(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TaskList(models.Model):
    title = models.CharField(max_length=100)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='lists')
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title

class Card(models.Model):

    PRIORITY_CHOICES = [
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    task_list = models.ForeignKey(
        TaskList,
        on_delete=models.CASCADE,
        related_name='cards'
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='assigned_cards'
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='media'
    )

    due_date = models.DateField(
        blank=True,
        null=True
    )

    position = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title

    @property
    def due_status(self):
        if not self.due_date:
            return 'Sin fecha límite'

        today = timezone.now().date()

        if self.due_date < today:
            return 'Vencida'
        elif self.due_date == today:
            return 'Vence hoy'
        else:
            return 'En tiempo'
    
    