# posts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment  
from posts.tasks import send_email_task

@receiver(post_save, sender=Comment)
def send_comment_notification(sender, instance, created, **kwargs):
    if created:  
        post_owner = instance.post.author           
        commenter_name = instance.user.username    
        post_title = instance.post.title           

        subject = "New Comment on Your Post"
        message = f"Hello {post_owner.username}, {commenter_name} commented on your post '{post_title}'."
        recipient_list = [post_owner.email]        

        
        send_email_task.delay(subject, message, recipient_list)
