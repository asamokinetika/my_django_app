
from django import forms
from .models import User
from django.contrib.auth.forms import (
    AuthenticationForm,UserCreationForm
)


class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
    
class UserCreateForm(UserCreationForm):
    class Meta:
        model=User
        fields=["email","name","password1","password2"]