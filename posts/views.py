from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils.dateparse import parse_date
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"
    ordering = ["-created_at"]
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get("title", "")
        author = self.request.GET.get("author", "")
        content = self.request.GET.get("content", "")
        start_date = self.request.GET.get("start_date", "")
        end_date = self.request.GET.get("end_date", "")

        if title:
            queryset = queryset.filter(title__istartswith=title) 
        if author:
            queryset = queryset.filter(author__username__iexact=author)
        if content:
            queryset = queryset.filter(content__icontains=content)  
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)

        return queryset.order_by("-created_at")  

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "posts/post_form.html"
    fields = ["title", "content"]
    success_url = reverse_lazy("posts:post-list")

    def form_valid(self, form):
        # Assign the currently logged-in user as the author
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"
