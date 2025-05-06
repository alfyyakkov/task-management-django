from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Task

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2', 'assigned_to']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['role', 'assigned_to']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'