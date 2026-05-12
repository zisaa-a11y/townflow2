from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.community_feed.views import CommentViewSet, PostViewSet

router = DefaultRouter()
router.register("posts", PostViewSet, basename="posts")
router.register("comments", CommentViewSet, basename="comments")

post_list = PostViewSet.as_view({"get": "list", "post": "create"})
post_detail = PostViewSet.as_view({"get": "retrieve", "delete": "destroy"})
post_like = PostViewSet.as_view({"post": "like", "delete": "like"})
post_comments = PostViewSet.as_view({"get": "comments", "post": "comments"})

urlpatterns = [
	path("feed/", post_list, name="feed-list-create"),
	path("feed/<uuid:pk>/", post_detail, name="feed-detail"),
	path("feed/<uuid:pk>/like/", post_like, name="feed-like"),
	path("feed/<uuid:pk>/comments/", post_comments, name="feed-comments"),
] + router.urls
