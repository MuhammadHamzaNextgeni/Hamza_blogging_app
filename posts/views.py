from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils.dateparse import parse_date
from .models import Post
from .filters import PostFilter
from .serializers import PostSerializer, CommentSerializer
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
from .models import Post, Comment, Like
from .forms import CommentForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from rest_framework.views import APIView
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class PostListView(JWTLoginRequiredMixin, ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"
    paginate_by = 6
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = Post.objects.all()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        queryset = self.filterset.qs

        if self.request.GET.get("my_posts") == "1":
            queryset = queryset.filter(author=self.request.user)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_params"] = self.request.GET
        return context


User = get_user_model()   

class AuthorSuggestionsView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get("q", "").strip()

        users = []
        if q:
            users = (
                User.objects
                .filter(username__istartswith=q)
                .order_by("username")
                .values_list("username", flat=True)[:10]
            )

        return JsonResponse({"results": list(users)})


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        user = self.request.user

        
        if user.is_authenticated:
            context['form'] = CommentForm()
            context['liked'] = post.likes.filter(user=user).exists()
        else:
            context['form'] = None
            context['liked'] = False

        # Fetch only top-level comments, prefetch replies
        context['comments'] = post.comments.filter(parent__isnull=True).prefetch_related('replies')
        return context

    
class AddCommentView(JWTLoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user

            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent = Comment.objects.get(id=parent_id)  

            comment.save()
        return redirect("posts:post-detail", pk=pk)


class ToggleLikeView(JWTLoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        like, created = post.likes.get_or_create(user=request.user)
        if not created:
            like.delete()
        return redirect("posts:post-detail", pk=pk)


class PostUpdateView(JWTLoginRequiredMixin, UpdateView):
    model = Post
    template_name = "posts/post_update.html"  
    fields = ["title", "content"]

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("You cannot update someone else's post.")
        return obj

    def get_success_url(self):

        return reverse("posts:post-detail", kwargs={"pk": self.object.pk})

class PostDeleteView(JWTLoginRequiredMixin, DeleteView):
    model = Post
    template_name = "posts/post_confirm_delete.html"  
    success_url = reverse_lazy("posts:post-list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            raise PermissionDenied("You cannot delete someone else's post.")
        return obj


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
    

class PostCommentCreateAPI(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_pk = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, pk=post_pk)
        parent_id = self.request.data.get('parent_id')

        parent_comment = None
        if parent_id:
            parent_comment = Comment.objects.get(id=parent_id)
        serializer.save(user=self.request.user, post=post, parent=parent_comment)

class PostToggleLikeAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_pk, format=None):
        post = get_object_or_404(Post, pk=post_pk)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
            return Response({"liked": False, "like_count": post.likes.count()})
        return Response({"liked": True, "like_count": post.likes.count()})
    
User = get_user_model()

class AuthorSuggestionsAPI(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get("q", "").strip()

        users = []
        if q:
            users = (
                User.objects
                .filter(username__istartswith=q)
                .order_by("username")
                .values("id", "username")[:10]   # include id + username
            )

        return JsonResponse({"results": list(users)})