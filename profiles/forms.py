import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from chores.models import Room

User = get_user_model()

class SignUpForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'first_name_input'})
    )
    last_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'last_name_input'})
    )
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'username_input'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password_input'})
    )
    room_pass = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'room_pass_input'})
    )

    def save(self):
        username = self.cleaned_data['username']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        password = self.cleaned_data['password']
        room_pass = self.cleaned_data['room_pass']

        user = User(username=username, first_name=first_name, last_name=last_name)
        user.set_password(password)
        entry_approved = False
        if Room.objects.filter(room_pass=room_pass).exists():
            room = Room.objects.get(room_pass=room_pass)
        else:
            room = Room.objects.create()
            entry_approved = True

        user.room = room
        user.entry_approved = entry_approved
        user.save()
        return user

    def is_valid_password(self, password):
        if len(password) < 8:
            return False

        if not re.search(r'[A-Z]', password):
            return False

        if not re.search(r'\d', password):
            return False

        return True
    
    def is_valid_username(self, username):
        return not User.objects.filter(username=username).exists()

    def is_valid_room_pass(self, room_pass):
        if room_pass:
            return Room.objects.filter(room_pass=room_pass).exists()
        else:
            return True

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        room_pass = cleaned_data.get('room_pass')

        if username and password:
            if not self.is_valid_password(password):
                print("not self.is_valid_password(password)")
                self.add_error('password', 'Password must be at least 8 characters long and contain at least one capital letter and one number.')
            
            if not self.is_valid_username(username):
                print("not self.is_valid_username(username)")
                self.add_error('username', 'username already exists')
            
            if not self.is_valid_room_pass(room_pass):
                self.add_error('room_pass', 'Invalid Room Pass')

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'username_input'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password_input'})
    )

    def is_valid_password(self, password):
        if len(password) < 8:
            return False

        if not re.search(r'[A-Z]', password):
            return False

        if not re.search(r'\d', password):
            return False

        return True

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            if not self.is_valid_password(password):
                self.add_error('password', 'Password must be at least 8 characters long and contain at least one capital letter and one number.')

            if not User.objects.filter(username=username).exists():
                self.add_error('username', 'username not found')

            user = authenticate(username=username, password=password)
            if user is not None:
                self.user = user
            else:
                self.add_error(None, 'Unable to login')

        return cleaned_data


    def get_user(self):
        return self.user
