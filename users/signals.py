from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from posts.tasks import send_email_task  # import your Celery task

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:  # only on new user signup
        subject = "Welcome to Blogging Platform"
        message = f"Hello {instance.username}, welcome to our blogging platform!"
        recipient_list = [instance.email]

        # send via Celery
        send_email_task.delay(subject, message, recipient_list)
