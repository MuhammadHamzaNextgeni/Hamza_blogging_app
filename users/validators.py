from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password

def custom_email_validator(email):
        if "@" not in email:   
            raise ValidationError("Email must contain '@'")
        if not email.endswith(".com"):
            raise ValidationError("Email must end with '.com'")


def custom_password_hasher(raw_password: str) -> str:
    """
    Hash the raw password using Django's built-in hasher.
    """
    return make_password(raw_password)

def verify_password(raw_password: str, hashed_password: str) -> bool:
    """
    Verify a raw password against the stored hashed password.
    """
    return check_password(raw_password, hashed_password)


