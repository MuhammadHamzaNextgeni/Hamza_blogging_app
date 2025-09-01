from django.core.exceptions import ValidationError

def custom_email_validator(self,email):
        if "@" not in email:   
            raise ValidationError("Email must contain '@'")
        if not email.endswith(".com"):
            raise ValidationError("Email must end with '.com'")