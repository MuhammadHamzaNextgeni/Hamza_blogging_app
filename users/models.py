from django.contrib.auth.models import AbstractUser
from django.db import models
from users.validators import custom_email_validator,custom_password_hasher,verify_password
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
    password = models.CharField(max_length=128)  

    def set_password(self, raw_password):
        """
        Hash the password using our helper and save it.
        """
        self.password = custom_password_hasher(raw_password)

    def check_password(self, raw_password) -> bool:
        """
        Verify a raw password using our helper.
        """
        return verify_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        
        if not self.password.startswith("pbkdf2_"):  
            self.password = custom_password_hasher(self.password)
        super().save(*args, **kwargs)
    
    



    
        








    

