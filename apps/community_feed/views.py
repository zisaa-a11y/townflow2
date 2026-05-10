from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action

from apps.community_feed.models import Post, PostComment, PostLike
from apps.community_feed.serializers import PostCommentSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["category", "is_published"]
    search_fields = ["content", "author__full_name"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        return (
            Post.objects.select_related("author")
            .prefetch_related("likes", "comments")
            .filter(is_published=True)
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"], url_path="like")
    def like(self, request, pk=None):
        post = self.get_object()
        PostLike.objects.get_or_create(post=post, user=request.user)
        return self.list(request)

    @action(detail=True, methods=["post"], url_path="unlike")
    def unlike(self, request, pk=None):
        post = self.get_object()
        PostLike.objects.filter(post=post, user=request.user).delete()
        return self.list(request)


class CommentViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PostCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["post"]

    def get_queryset(self):
        return PostComment.objects.select_related("user", "post")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
