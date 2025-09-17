# posts/mixins.py
from django.shortcuts import redirect
from django.contrib import messages
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class JWTLoginRequiredMixin:
    """
    A mixin to authenticate users via JWT for Django template views.
    """

    def dispatch(self, request, *args, **kwargs):
        token = request.COOKIES.get("access_token")  # Read token from cookie
        if not token:
            messages.error(request, "You must log in to access this page.")
            return redirect("users:login")

        try:
            user_auth_tuple = JWTAuthentication().authenticate(request)
            if user_auth_tuple is not None:
                request.user = user_auth_tuple[0]  # set user from JWT
            else:
                messages.error(request, "Authentication required. Please log in.")
                return redirect("users:login")
        except AuthenticationFailed:
            messages.error(request, "Invalid or expired token. Please log in again.")
            return redirect("users:login")

        return super().dispatch(request, *args, **kwargs)
