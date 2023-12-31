from asyncio import tasks
from email import message
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from chores.constants import TASK_STATUS_CHOICES, TASK_STATUS_COMPLETED, TASK_STATUS_DONE, TASK_STATUS_IN_PROGRESS
from chores.forms import AddRoommateForm, TaskForm
from django.db.models import Q
from chores.models import Room, Task
from django.contrib import messages

User = get_user_model()


@login_required(login_url='login_view')
def home(request):
    context = {}
    return render(request, "chores/home.html", context)


@login_required(login_url='login_view')
def approve_user(request, user_id):
    requesting_user = get_object_or_404(User, id=int(user_id))
    if requesting_user.room.id == request.user.room.id:
        requesting_user.entry_approved = True
        requesting_user.save()
        messages.info(request, f"{requesting_user.username} has been added to your room")
    else:
        messages.error(request, "Something went wrong")

    return redirect("my-room")


@login_required(login_url='login_view')
def my_room(request):
    current_user = request.user
    context = {}
    context["room"] = current_user.room
    context["entry_approved"] = current_user.entry_approved
    context["roommates"] = User.objects.filter(room=current_user.room, entry_approved=True).exclude(id=current_user.id)
    context["roommates_approval_required"] = User.objects.filter(room=current_user.room, entry_approved=False).exclude(id=current_user.id)
    context["tasks"] = Task.objects.filter(room=current_user.room).order_by("-updated")
    context["create_task_form"] = TaskForm(current_user)
    context["add_roommate_form"] = AddRoommateForm(current_user)

    return render(request, "chores/pages/my_room.html", context)


@login_required(login_url='login_view')
def my_tasks(request):
    context = {}
    filter_expression = Q(reporter=request.user) | Q(assigned_to=request.user)
    context["tasks"] = Task.objects.filter(filter_expression).order_by("-created")
    return render(request, "chores/pages/tasks/my_tasks.html", context)

@login_required(login_url='login_view')
def task(request, task_id):
    if not request.user.entry_approved:
        return redirect("my-room")
    current_user = request.user
    context = {}
    task = get_object_or_404(Task, id=int(task_id))
    if request.method == "POST":
        task.title = request.POST.get("title", "")
        task.description = request.POST.get("description", "")
        assignee_id = request.POST.get("assignee_id")
        assigned_to = get_object_or_404(User, id=int(assignee_id))
        task.assigned_to = assigned_to
        task.status = request.POST.get("status", None)
        task.save()
        messages.success(request, "Task updated")
        return redirect(f"/tasks/{task.id}")

    context["task"] = task
    context["assigned_to_options"] = User.objects.filter(room=current_user.room, entry_approved=True)
    context["status_options"] = TASK_STATUS_CHOICES
    context["task"] = task
    return render(request, "chores/pages/tasks/task.html", context)

@login_required(login_url='login_view')
def create_task(request):

    context = {}
    if request.method == "POST":
        form = TaskForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Task Created")
        else:
            messages.error(request, "Not valid form")
    else:
        form = TaskForm(request.user)
    context["create_task_form"] = form
    return redirect("my-room")

@login_required(login_url='login_view')
def delete_task(request):
    messages.info("Task Deleted")
    return redirect("my-room")

@login_required(login_url='login_view')
def add_roommate(request):
    if request.method == "POST":
        form = AddRoommateForm(request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Roommate added")
        else:
            messages.error(request, "Something went wrong")
    
    return redirect("my-room")


@login_required(login_url='login_view')
def my_account(request):
    current_user = request.user
    context = {}
    context["done_tasks"] = Task.objects.filter(assigned_to=current_user, status=TASK_STATUS_DONE).count()
    context["approved_tasks"] = Task.objects.filter(assigned_to=current_user, status=TASK_STATUS_COMPLETED).count()
    context["pending_tasks"] = Task.objects.filter(assigned_to=current_user, status=TASK_STATUS_IN_PROGRESS).count()
    return render(request, "chores/pages/my_account.html", context)