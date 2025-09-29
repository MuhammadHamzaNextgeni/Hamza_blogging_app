from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import custom_email_validator
from users.validators import custom_email_validator,custom_password_hasher,verify_password

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)  
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        validators=[custom_email_validator]
    )
    bio = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = 'email'       
    REQUIRED_FIELDS = []          

    def set_password(self, raw_password):
        self.password = custom_password_hasher(raw_password)

    def check_password(self, raw_password) -> bool:
        return verify_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        if not self.password.startswith("pbkdf2_"):
            self.password = custom_password_hasher(self.password)
        super().save(*args, **kwargs)

    
    



    
        








    

