from django.contrib import admin

from chores.models import Room, Task

admin.site.register(Task)
admin.site.register(Room)