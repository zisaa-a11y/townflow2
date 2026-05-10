from rest_framework import serializers

from apps.community_feed.models import Post, PostComment, PostLike


class PostCommentSerializer(serializers.ModelSerializer):
    commenter_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = PostComment
        fields = ["id", "post", "user", "commenter_name", "body", "created_at"]
        read_only_fields = ["id", "user", "commenter_name", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.full_name", read_only=True)
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "author_name",
            "category",
            "content",
            "image",
            "is_published",
            "likes_count",
            "comments_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "author", "author_name", "likes_count", "comments_count", "created_at", "updated_at"]


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ["id", "post", "user"]
        read_only_fields = ["id", "user"]
