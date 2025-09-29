from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_username(self):
        """
        Override the default uniqueness check for username,
        so duplicate usernames are allowed.
        """
        username = self.cleaned_data.get("username")
        
        return username
