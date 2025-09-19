"""
from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path("api/login/", views.LoginAPIView.as_view(), name="api-login"),
    path("api/logout/", views.LogoutAPIView.as_view(), name="api-logout"),
    
    path('dashboard/', views.dashboard_view, name='dashboard'),  

]
"""

from django.urls import path
from .views import login_view, logout_view, signup_view, home_view, dashboard_view

app_name = "users"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("signup/", signup_view, name="signup"),  # this fixes the NoReverseMatch
    path("dashboard/", dashboard_view, name="dashboard"),
    path("", home_view, name="home"),
]





