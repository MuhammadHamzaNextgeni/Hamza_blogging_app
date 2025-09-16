from django.urls import path
from .views import PostListView, PostCreateView, PostDetailView

app_name = "posts"

urlpatterns = [
    path("", PostListView.as_view(), name="post-list"),
    path("new/", PostCreateView.as_view(), name="post-create"),  
    path("<int:pk>/", PostDetailView.as_view(), name="post-detail"),

]
