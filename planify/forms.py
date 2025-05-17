from django import forms
from django.contrib.auth import get_user_model

from planify.models import Task

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Введите пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')

        return cd['password2']


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_title', 'task_description', 'task_status', 'task_priority', 'task_due_date']


class TaskEditForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['task_owner', 'task_created_at', 'task_updated_at']
        widgets = {
            'task_due_date': forms.TextInput(attrs={'type': 'text', 'id': 'id_task_due_date'}),
            'task_description': forms.Textarea(attrs={'id': 'id_task_description'}),
        }

