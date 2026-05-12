from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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

    @action(detail=True, methods=["post", "delete"], url_path="like")
    def like(self, request, pk=None):
        post = self.get_object()
        if request.method.lower() == "delete":
            PostLike.objects.filter(post=post, user=request.user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        PostLike.objects.get_or_create(post=post, user=request.user)
        return Response(self.get_serializer(post).data)

    @action(detail=True, methods=["post"], url_path="unlike")
    def unlike(self, request, pk=None):
        post = self.get_object()
        PostLike.objects.filter(post=post, user=request.user).delete()
        return Response(self.get_serializer(post).data)

    @action(detail=True, methods=["get", "post"], url_path="comments")
    def comments(self, request, pk=None):
        post = self.get_object()
        if request.method.lower() == "post":
            serializer = PostCommentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        queryset = PostComment.objects.select_related("user", "post").filter(post=post)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PostCommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = PostCommentSerializer(queryset, many=True)
        return Response(serializer.data)


class CommentViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PostCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["post"]

    def get_queryset(self):
        return PostComment.objects.select_related("user", "post")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
