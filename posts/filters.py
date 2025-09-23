from django.db.models import Q
from .models import Post
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

class PostFilter:
    def __init__(self, params, queryset=None):
        self.params = params
        self.queryset = queryset if queryset is not None else Post.objects.all()

    @property
    def qs(self):
        title = self.params.get("title", "")
        author = self.params.get("author", "")
        content = self.params.get("content", "")
        start_date = self.params.get("start_date", "")
        end_date = self.params.get("end_date", "")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__istartswith=title)
        if author:
            queryset = queryset.filter(author__username__istartswith=author)
        if content:
            queryset = queryset.filter(content__icontains=content)
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)

        return queryset.order_by("-created_at")