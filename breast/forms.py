from django.forms import ModelForm
from .models import CustomUser


class LoginForm(ModelForm):
    
    class Meta:
        model = CustomUser
        fields = ("username","password")
