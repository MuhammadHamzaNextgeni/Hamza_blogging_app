from django.shortcuts import render, redirect   
from django.contrib.auth.models import User     
from django.contrib.auth.forms import UserCreationForm  
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login,authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import constants

# Create your views here.

def home_view(request):
    return render(request, "home.html")

def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, constants.ACCOUNT_CREATION_SUCCESS_MESSAGE)  
            
            # Redirect to login page after successful registration
            return redirect("users:login")

        else:
            print(form.errors)  
    else:
        form = CustomUserCreationForm()
    
    return render(request, "users/signup.html", {"form": form})



User = get_user_model()

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
            return render(request, "users/login.html")

        # Authenticate using Django's built-in method
        user = authenticate(request, username=user_obj.username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect("users:dashboard")  # redirect to dashboard
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, "users/login.html")


def logout_view(request):
    logout(request)  
    messages.success(request, constants.LOGOUT_SUCCESS_MESSAGE)  
    return redirect("users:login")  


@login_required
def dashboard_view(request):
    return render(request, "users/dashboard.html")


