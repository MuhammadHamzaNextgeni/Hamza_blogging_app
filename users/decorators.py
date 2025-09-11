import jwt
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.timezone import now
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

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
            if exp and datetime.utcfromtimestamp(exp) < datetime.utcnow():
                messages.error(request, "Session expired. Please log in again.")
                return redirect("users:login")

            
            user_id = payload.get("user_id")
            request.user = User.objects.get(id=user_id)

            # Token valid → allow access
            return view_func(request, *args, **kwargs)

        except User.DoesNotExist:
            messages.error(request, "User not found. Please log in again.")
            return redirect("users:login")
        except jwt.ExpiredSignatureError:
            messages.error(request, "Session expired. Please log in again.")
            return redirect("users:login")
        except jwt.InvalidTokenError:
            messages.error(request, "Invalid authentication. Please log in again.")
            return redirect("users:login")

    return wrapper
