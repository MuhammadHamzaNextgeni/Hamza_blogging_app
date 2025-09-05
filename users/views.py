from django.shortcuts import render, redirect   
from django.contrib.auth.models import User     
from django.contrib.auth.forms import UserCreationForm  
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login,authenticate
from django.contrib.auth import get_user_model
from django.contrib import messages
from . import constants
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .decorators import jwt_login_required
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.decorators import login_required



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

        if not email or not password:
            messages.error(request, "Please enter email and password.")
            return render(request, "users/login.html")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
            return render(request, "users/login.html")

        if not user.check_password(password):
            messages.error(request, "Invalid email or password.")
            return render(request, "users/login.html")

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Set tokens in HttpOnly cookies
        response = redirect("users:dashboard")
        response.set_cookie("access_token", access_token, httponly=True, samesite="Strict")
        response.set_cookie("refresh_token", str(refresh), httponly=True, samesite="Strict")

        messages.success(request, "You have successfully logged in.")
        return response

    return render(request, "users/login.html")


def logout_view(request):
    response = redirect("users:login")
    # Clear the JWT cookies
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    messages.success(request, "You have successfully logged out.")
    return response


@login_required
def dashboard_view(request):
    return render(request, "users/dashboard.html")


@jwt_login_required
def dashboard_view(request):
    return render(request, "users/dashboard.html")




