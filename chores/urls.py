from django.urls import path
from chores import views


urlpatterns = [
    path("", views.home, name="home"),
    path("my-room/", views.my_room, name="my-room"),

    path("my-tasks/", views.my_tasks, name="my-tasks"),
    path("tasks/<str:task_id>/", views.task, name="tasks"),
    path("create_task/", views.create_task, name="create-task"),
    path("delete_task/<str:task_id>", views.delete_task, name="delete-task"),

    path("add_roommate/", views.add_roommate, name="add-roommate"),

    path("my-account/", views.my_account, name="my-account"),

    path("approve/<str:user_id>/", views.approve_user, name="approve-user"),
]
