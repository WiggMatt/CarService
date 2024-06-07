from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Client


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Client
        fields = ['bio', 'username', 'phone_number', 'license_num', 'password1', 'password2']
        widgets = {
            'bio': forms.TextInput(attrs={
                'placeholder': 'ФИО',
                'class': 'form-control'
            }),
            'username': forms.TextInput(attrs={
                'placeholder': 'Эл. почта',
                'class': 'form-control'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Номер телефона',
                'class': 'form-control'
            }),
            'license_num': forms.TextInput(attrs={
                'placeholder': 'Номер ВУ',
                'class': 'form-control'
            }),
            'password1': forms.PasswordInput(attrs={
                'placeholder': 'Пароль',
                'class': 'form-control'
            }),
            'password2': forms.PasswordInput(attrs={
                'placeholder': 'Повтор пароля',
                'class': 'form-control'
            })
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Email",
        max_length=100,
        widget=forms.EmailInput(attrs={'placeholder': 'Эл. почта'}),
    )
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
    )

    error_messages = {
        'invalid_login': "Пожалуйста, введите правильные почту и пароль. "
                         "Обратите внимание, что оба поля могут быть чувствительны к регистру.",
    }

