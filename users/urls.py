
from django.urls import path
from .views import login_view, logout_view, signup_view, home_view, dashboard_view, get_user_by_id

app_name = "users"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("signup/", signup_view, name="signup"),  
    path("dashboard/", dashboard_view, name="dashboard"),
    path("", home_view, name="home"),
    path('api/<int:user_id>/',get_user_by_id, name='get_user_by_id'),
]





