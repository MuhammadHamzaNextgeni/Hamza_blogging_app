from django.urls import path
from .views import PostListView, PostCreateView, PostDetailView, PostListAPI, PostDetailAPI, PostCreateAPI, PostUpdateView, PostUpdateAPI,PostDeleteView, PostDeleteAPI

app_name = "posts"

urlpatterns = [
    path("", PostListView.as_view(), name="post-list"),
    path("new/", PostCreateView.as_view(), name="post-create"),  
    path("<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("<int:pk>/edit/", PostUpdateView.as_view(), name="post-update"),
    path("<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    # endpoints for json 

    path("api/", PostListAPI.as_view(), name="api-post-list"),
    path("api/new/", PostCreateAPI.as_view(), name="api-post-create"),
    path("api/<int:pk>/", PostDetailAPI.as_view(), name="api-post-detail"),

    path("api/<int:pk>/update/", PostUpdateAPI.as_view(), name="api-post-update"),
    
    path("api/<int:pk>/delete/", PostDeleteAPI.as_view(), name="api-post-delete"),


]




