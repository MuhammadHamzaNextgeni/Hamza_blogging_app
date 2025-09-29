from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True 


class Post(TimeStampedModel):   
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title


class Comment(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )  

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"



class Like(TimeStampedModel):   
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")

    
    updated_at = None  

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"

