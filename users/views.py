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
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth import get_user_model, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer  

# Create your views here.

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        data = response.data

        refresh_token = data.get("refresh")
        access_token = data.get("access")

        if refresh_token and access_token:
            # Set HttpOnly cookies
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,  
                samesite="Strict",
                max_age=30*60  
            )
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite="Strict",
                max_age=5*24*60*60  
            )

            # Remove tokens from response body
            response.data = {"detail": "Login successful"}

        return response


# --------------------
# REFRESH VIEW: uses cookie to refresh access token
# --------------------
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"detail": "No refresh token cookie found"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(data={"refresh": refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        access_token = serializer.validated_data.get("access")

        # Update access token cookie
        response = Response({"detail": "Token refreshed successfully"}, status=status.HTTP_200_OK)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="Strict",
            max_age=30*60  # match access token lifetime
        )
        return response

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

@csrf_exempt  
def login_view(request):
    if request.method == "POST":
        import json

        # Detect if JSON body is sent
        if request.content_type == "application/json":
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")
        else:
            email = request.POST.get("email")
            password = request.POST.get("password")

        if not email or not password:
            if request.content_type == "application/json":
                return JsonResponse({"error": constants.ENTER_EMAIL_PASSWORD_MESSAGE}, status=400)
            messages.error(request, constants.ENTER_EMAIL_PASSWORD_MESSAGE)
            return render(request, "users/login.html")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            if request.content_type == "application/json":
                return JsonResponse({"error": constants.NO_ACCOUNT_FOUND}, status=404)
            messages.error(request, constants.NO_ACCOUNT_FOUND)
            return render(request, "users/login.html")

        if not user.check_password(password):
            if request.content_type == "application/json":
                return JsonResponse({"error": constants.INVALID_EMAIL_MESSAGE}, status=400)
            messages.error(request, constants.INVALID_EMAIL_MESSAGE)
            return render(request, "users/login.html")

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Browser response
        if request.content_type != "application/json":
            response = redirect("users:dashboard")
            response.set_cookie("access_token", access_token, httponly=True, samesite="Strict")
            response.set_cookie("refresh_token", str(refresh), httponly=True, samesite="Strict")
            messages.success(request, constants.LOG_IN_SUCCESS_MESSAGE)
            return response

        # JSON response for API clients
        return JsonResponse(
            {
                "access": access_token,
                "refresh": str(refresh),
                "message": constants.LOG_IN_SUCCESS_MESSAGE,
            }
        )

    return render(request, "users/login.html")



def logout_view(request):
    if request.content_type == "application/json":
        return JsonResponse({"message": constants.LOGOUT_SUCCESS_MESSAGE})
    
    response = redirect("users:login")
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    messages.success(request, constants.LOGOUT_SUCCESS_MESSAGE)
    return response


@jwt_login_required
def dashboard_view(request):
    return render(request, "users/dashboard.html")


@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def get_user_by_id(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

