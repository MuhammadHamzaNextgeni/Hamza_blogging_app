from django.urls import path
from .views import PostListView, PostCreateView, PostDetailView, PostListAPI, PostDetailAPI, PostCreateAPI, PostUpdateView, PostUpdateAPI,PostDeleteView, PostDeleteAPI, PostCommentCreateAPI,PostToggleLikeAPI,AddCommentView,ToggleLikeView,AuthorSuggestionsView,AuthorSuggestionsAPI

app_name = "posts"

urlpatterns = [
    path("", PostListView.as_view(), name="post-list"),
    path("new/", PostCreateView.as_view(), name="post-create"),  
    path("<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("<int:pk>/edit/", PostUpdateView.as_view(), name="post-update"),
    path("<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path('post/<int:pk>/comment/', AddCommentView.as_view(), name='add_comment'),
    path('post/<int:pk>/like/', ToggleLikeView.as_view(), name='toggle_like'),
    path("author-suggestions/", AuthorSuggestionsView.as_view(), name="author-suggestions"),

 # endpoints for json 

    path("api/", PostListAPI.as_view(), name="api-post-list"),
    path("api/new/", PostCreateAPI.as_view(), name="api-post-create"),
    path("api/<int:pk>/", PostDetailAPI.as_view(), name="api-post-detail"),
    path("api/<int:pk>/update/", PostUpdateAPI.as_view(), name="api-post-update"),
    path("api/<int:pk>/delete/", PostDeleteAPI.as_view(), name="api-post-delete"),
    path('api/<int:post_pk>/comments/', PostCommentCreateAPI.as_view(), name='api-comment-create'),
    path('api/<int:post_pk>/like/', PostToggleLikeAPI.as_view(), name='api-toggle-like'),
    path("api/author-suggestions/", AuthorSuggestionsAPI.as_view(), name="author-suggestions-api"),


]




