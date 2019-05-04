from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth import get_user_model


class RegisterForm(UserCreationForm):
    class Meta:
        fields = ('username','password1','password2')
        model = get_user_model()

class LoginForm(AuthenticationForm):
    class Meta:
        fields = ('username','password')
        model = get_user_model()