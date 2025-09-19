from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.shortcuts import redirect
from django.contrib import messages

class JWTLoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        token = request.COOKIES.get("access_token")
        if not token:
            messages.error(request, "You must log in to access this page.")
            return redirect("users:login")

        # Temporarily add Authorization header for DRF JWTAuthentication
        request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"

        try:
            user_auth_tuple = JWTAuthentication().authenticate(request)
            if user_auth_tuple is not None:
                request.user = user_auth_tuple[0]  # Set user from JWT
            else:
                messages.error(request, "Authentication required. Please log in.")
                return redirect("users:login")
        except AuthenticationFailed:
            messages.error(request, "Invalid or expired token. Please log in again.")
            return redirect("users:login")

        return super().dispatch(request, *args, **kwargs)

