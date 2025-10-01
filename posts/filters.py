from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .models import Post

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
            author = author.lstrip("@").strip()   
            if author:
                queryset = queryset.filter(author__username__istartswith=author)

        if content:
            search_vector = SearchVector("title", "content")
            search_query = SearchQuery(content)

            queryset = (
                queryset
                .annotate(rank=SearchRank(search_vector, search_query))
                .filter(rank__gte=0.1)
                .order_by("-rank", "-created_at")
            )

            if not queryset.exists():
                queryset = self.queryset.filter(
                    Q(title__icontains=content) | Q(content__icontains=content)
                )

        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)

        return queryset.order_by("-created_at")