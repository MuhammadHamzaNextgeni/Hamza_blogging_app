import jwt
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.timezone import now
from datetime import datetime

def jwt_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get("access_token")

        if not token:
            messages.error(request, "You must log in first.")
            return redirect("users:login")

        try:
            # Decode token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            # Check expiry
            exp = payload.get("exp")
            if exp and datetime.utcfromtimestamp(exp) < now().replace(tzinfo=None):
                messages.error(request, "Session expired. Please log in again.")
                return redirect("users:login")

            # Token valid → allow access
            return view_func(request, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            messages.error(request, "Session expired. Please log in again.")
            return redirect("users:login")
        except jwt.InvalidTokenError:
            messages.error(request, "Invalid authentication. Please log in again.")
            return redirect("users:login")

    return wrapper
