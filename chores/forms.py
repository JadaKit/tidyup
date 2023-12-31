

from cProfile import label
from django import forms
from django.contrib.auth import get_user_model

from chores.constants import TASK_STATUS_CHOICES
from chores.models import Task
from chores.utils import get_default_due_date

User = get_user_model()


class TaskForm(forms.Form):
    title = forms.CharField(
        label="Title",
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'title_input'})
    )
    description = forms.CharField(
        label="Description",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'description_input'})
    )
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.none(),
        empty_label="Select Roommate",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'assigned_to_input'})
    )
    reporter = forms.ModelChoiceField(
        queryset=User.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'assigned_to_input', 'disabled':'disabled'})
    )
    status = forms.CharField(
        label="Status",
        required=True,
        widget=forms.Select(choices=TASK_STATUS_CHOICES, attrs={'class': 'form-select', 'id': 'status_input'}),
    )
    due_date = forms.DateTimeField(
        label="Due Date",
        required=True,
        widget=forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'id': 'due_date_input', 'type':'datetime-local'}),
        # input_formats=['%Y-%m-%d %H:%M:%S'],  # Specify the input format if needed
    )

    def __init__(self, user, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['assigned_to'].queryset = User.objects.filter(room=self.user.room, entry_approved=True)
        self.fields['reporter'].queryset = User.objects.filter(id=user.id)
        self.fields['reporter'].initial = self.user.id
        self.fields['due_date'].initial = get_default_due_date()

    def save(self):
        task = Task.objects.create(
            title=self.cleaned_data['title'],
            description=self.cleaned_data['description'],
            assigned_to=self.cleaned_data['assigned_to'],
            reporter_id=self.cleaned_data['reporter'],
            status=self.cleaned_data['status'],
            due_date=self.cleaned_data['due_date'],
            room = self.user.room
        )

        return task


    def clean(self):
        cleaned_data = super().clean()
        reporter = cleaned_data.get('reporter')

        if reporter is None:
            cleaned_data["reporter"] = self.user.id

        
        return cleaned_data

class AddRoommateForm(forms.Form):
    roommate = forms.ModelChoiceField(
        queryset=User.objects.none(),
        empty_label="Select Roommate",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'roommate_input'})
    )

    def __init__(self, user, *args, **kwargs):
        super(AddRoommateForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['roommate'].queryset = User.objects.filter(room__isnull=True).exclude(id=self.user.id)

    def save(self):
        roommate = self.cleaned_data['roommate']
        roommate.room = self.user.room
        roommate.save()

        return roommate


    def clean(self):
        cleaned_data = super().clean()
        roommate = cleaned_data.get('roommate')
        print("clean roommate", roommate)        
        return cleaned_data