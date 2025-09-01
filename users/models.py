from django.contrib.auth.models import AbstractUser
from django.db import models
from users.validators import custom_email_validator
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


# Create your models here.

class User(AbstractUser):
    # Adding the new bio field 
    bio = models.TextField(blank=True, null=True)  
    email = models.TextField(
        blank=False,
        null=False,
        validators=[custom_email_validator]
    )



    
        








