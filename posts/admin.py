from django.contrib import admin
from django.db.models import Count  
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


# Custom list filters for Comments
class CommentsCountFilter(admin.SimpleListFilter):
    title = "Comments Count"
    parameter_name = "comments_count"

    def lookups(self, request, model_admin):
        return (
            ("1-100", "1 to 100"),
            ("101-300", "101 to 300"),
            ("301+", "301 and above"),  # Added 301+ range
        )

    def queryset(self, request, queryset):
        if self.value() == "1-100":
            return queryset.annotate(num_comments=Count("comments")).filter(num_comments__gte=1, num_comments__lte=100)
        elif self.value() == "101-300":
            return queryset.annotate(num_comments=Count("comments")).filter(num_comments__gte=101, num_comments__lte=300)
        elif self.value() == "301+":
            return queryset.annotate(num_comments=Count("comments")).filter(num_comments__gte=301)
        return queryset


# Custom list filters for Likes
class LikesCountFilter(admin.SimpleListFilter):
    title = "Likes Count"
    parameter_name = "likes_count"

    def lookups(self, request, model_admin):
        return (
            ("1-100", "1 to 100"),
            ("101-300", "101 to 300"),
            ("301+", "301 and above"),  # Added 301+ range
        )

    def queryset(self, request, queryset):
        if self.value() == "1-100":
            return queryset.annotate(num_likes=Count("likes")).filter(num_likes__gte=1, num_likes__lte=100)
        elif self.value() == "101-300":
            return queryset.annotate(num_likes=Count("likes")).filter(num_likes__gte=101, num_likes__lte=300)
        elif self.value() == "301+":
            return queryset.annotate(num_likes=Count("likes")).filter(num_likes__gte=301)
        return queryset


# Post admin
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "updated_at", "comments_count", "likes_count")
    search_fields = ("title", "content", "author__username")
    list_filter = ("author", "created_at", "updated_at", CommentsCountFilter, LikesCountFilter)
    inlines = [CommentInline, LikeInline]

    def comments_count(self, obj):
        return obj.comments.count()
    comments_count.short_description = "Comments"

    def likes_count(self, obj):
        return obj.likes.count()
    likes_count.short_description = "Likes"


# Comment admin
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "short_content", "created_at")
    search_fields = ("content", "user__username", "post__title")
    list_filter = ("user", "created_at")

    def short_content(self, obj):
        return obj.content[:50] + ("..." if len(obj.content) > 50 else "")
    short_content.short_description = "Content"


# Like admin
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "created_at")
    search_fields = ("user__username", "post__title")
    list_filter = ("user", "created_at")

