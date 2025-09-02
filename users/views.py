from django.shortcuts import render
from django.shortcuts import render, redirect   
from django.contrib.auth.models import User     
from django.contrib.auth.forms import UserCreationForm  
from .forms import CustomUserCreationForm
from django.contrib import messages             
from .messages import ACCOUNT_CREATION_SUCCESS_MESSAGE
# Create your views here.

def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ACCOUNT_CREATION_SUCCESS_MESSAGE)  

            form = CustomUserCreationForm()  # reset form after success
             
        else:
            print(form.errors)  
    else:
        form = CustomUserCreationForm()
    return render(request, "users/signup.html", {"form": form})




