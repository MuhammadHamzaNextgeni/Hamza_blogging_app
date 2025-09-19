from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils.dateparse import parse_date
from .models import Post
from .filters import PostFilter
from .serializers import PostSerializer
from django.http import JsonResponse
from rest_framework.response import Response
from .mixins import JWTLoginRequiredMixin
from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer
from django.urls import reverse
from django.views.generic import DeleteView
from django.core.exceptions import PermissionDenied
from rest_framework import status


class PostListView(JWTLoginRequiredMixin, ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"
    paginate_by = 5
    ordering = ["-created_at"]

    def get_queryset(self):
        # Use the PostFilter class
        self.filterset = PostFilter(self.request.GET, queryset=Post.objects.all())
        return self.filterset.qs  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_params"] = self.request.GET 
        return context

class PostCreateView(JWTLoginRequiredMixin, CreateView):
    model = Post
    template_name = "posts/post_form.html"
    fields = ["title", "content"]
    success_url = reverse_lazy("posts:post-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDetailView(JWTLoginRequiredMixin, DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"


class PostUpdateView(JWTLoginRequiredMixin, UpdateView):
    model = Post
    template_name = "posts/post_update.html"  # You can also use post_update.html
    fields = ["title", "content"]

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("You cannot update someone else's post.")
        return obj

    def get_success_url(self):
        # Redirect to the post detail page after updating
        return reverse("posts:post-detail", kwargs={"pk": self.object.pk})

class PostDeleteView(JWTLoginRequiredMixin, DeleteView):
    model = Post
    template_name = "posts/post_confirm_delete.html"  # Confirmation template
    success_url = reverse_lazy("posts:post-list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            raise PermissionDenied("You cannot delete someone else's post.")
        return obj


# Below the views for crud for json 

class PostListAPI(generics.ListAPIView):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostDetailAPI(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostCreateAPI(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostUpdateAPI(generics.RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.author != self.request.user:
            raise PermissionDenied("You cannot update someone else's post.")
        return obj

class PostDeleteAPI(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"

    def get_object(self):
        obj = super().get_object()
        if obj.author != self.request.user:
            raise PermissionDenied("You cannot delete someone else's post.")
        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Post deleted successfully."}, status=status.HTTP_200_OK)