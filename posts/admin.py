from django.contrib import admin
from .models import Post, Comment, Like

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "updated_at")
    search_fields = ("title", "content", "author__username")  
    list_filter = ("author", "created_at", "updated_at")      


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "created_at")
    search_fields = ("content", "user__username", "post__title")
    list_filter = ("user", "created_at")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "created_at")
    search_fields = ("user__username", "post__title")
    list_filter = ("user", "created_at")

