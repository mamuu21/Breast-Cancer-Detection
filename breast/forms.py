from django.forms import ModelForm
from .models import CustomUser
from django import forms


class LoginForm(ModelForm):
    
    class Meta:
        model = CustomUser
        fields = ("username","password")
