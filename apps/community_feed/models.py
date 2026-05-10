from django.conf import settings
from django.db import models

from common.constants.enums import FeedCategory
from common.db.models import BaseModel
from common.validators.files import validate_image_upload


class Post(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    category = models.CharField(max_length=20, choices=FeedCategory.CHOICES, db_index=True)
    content = models.TextField()
    image = models.ImageField(upload_to="community/posts/", blank=True, null=True, validators=[validate_image_upload])
    is_published = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["category", "created_at"])]


class PostLike(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post_likes")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["post", "user"], name="unique_post_like")]


class PostComment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post_comments")
    body = models.TextField()

    class Meta:
        ordering = ["created_at"]
