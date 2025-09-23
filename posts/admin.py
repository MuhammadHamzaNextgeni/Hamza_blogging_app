from django.contrib import admin
from .models import Post, Comment, Like

# Inline models for Post admin
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    fields = ("user", "content", "created_at")
    readonly_fields = ("created_at",)
    show_change_link = True


class LikeInline(admin.TabularInline):
    model = Like
    extra = 0
    fields = ("user", "created_at")
    readonly_fields = ("created_at",)
    show_change_link = True


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "updated_at", "comments_count", "likes_count")
    search_fields = ("title", "content", "author__username")
    list_filter = ("author", "created_at", "updated_at")
    inlines = [CommentInline, LikeInline]

    def comments_count(self, obj):
        return obj.comments.count()
    comments_count.short_description = "Comments"

    def likes_count(self, obj):
        return obj.likes.count()
    likes_count.short_description = "Likes"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "short_content", "created_at")
    search_fields = ("content", "user__username", "post__title")
    list_filter = ("user", "created_at")

    def short_content(self, obj):
        return obj.content[:50] + ("..." if len(obj.content) > 50 else "")
    short_content.short_description = "Content"


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "created_at")
    search_fields = ("user__username", "post__title")
    list_filter = ("user", "created_at")

