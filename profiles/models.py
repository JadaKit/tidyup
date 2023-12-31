from django.db import models
from django.contrib.auth.models import AbstractUser

from chores.models import Room


class User(AbstractUser):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    rating = models.FloatField(null=True)
    entry_approved = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username
