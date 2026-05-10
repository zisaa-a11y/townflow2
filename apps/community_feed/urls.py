from rest_framework.routers import DefaultRouter

from apps.community_feed.views import CommentViewSet, PostViewSet

router = DefaultRouter()
router.register("posts", PostViewSet, basename="posts")
router.register("comments", CommentViewSet, basename="comments")

urlpatterns = router.urls
