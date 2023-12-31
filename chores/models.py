from django.db import models
from chores.constants import (
    TASK_STATUS_CHOICES,
    TASK_STATUS_TODO
)
from django.conf import settings
from chores.utils import get_default_due_date, generate_random_string

class Room(models.Model):
    name = models.CharField(max_length=255, default="untitled")
    room_pass = models.CharField(max_length=30, default=generate_random_string)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=TASK_STATUS_CHOICES, default=TASK_STATUS_TODO)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name="tasks_assigned_to")
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks_reporter")
    due_date = models.DateTimeField(default=get_default_due_date)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    comments = models.ManyToManyField("UserComment", blank=True)


class UserComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
