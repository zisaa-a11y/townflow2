"""Tests for community feed module."""

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.community_feed.models import Post, PostLike, PostComment
from common.constants.enums import FeedCategory

User = get_user_model()


@pytest.fixture
def api_client():
    """Fixture providing an API client."""
    return APIClient()


@pytest.fixture
def user(db):
    """Fixture creating a test user."""
    return User.objects.create_user(
        email='test@example.com',
        password='testpass123',
        full_name='Test User'
    )


@pytest.fixture
def other_user(db):
    """Fixture creating another test user."""
    return User.objects.create_user(
        email='other@example.com',
        password='testpass123',
        full_name='Other User'
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Fixture providing authenticated API client."""
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.fixture
def post(db, user):
    """Fixture creating a test post."""
    return Post.objects.create(
        author=user,
        category=FeedCategory.NEWS,
        content='Test post content',
        is_published=True
    )


@pytest.mark.django_db
class TestCommunityFeed:
    """Test suite for community feed endpoints."""

    def test_create_post(self, authenticated_client):
        """Test creating a new post."""
        response = authenticated_client.post('/api/v1/community-feed/posts/', {
            'category': FeedCategory.NEWS,
            'content': 'New post content',
            'is_published': True
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['content'] == 'New post content'
        assert Post.objects.count() == 1

    def test_list_posts(self, authenticated_client, post):
        """Test listing posts."""
        response = authenticated_client.get('/api/v1/community-feed/posts/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    def test_list_posts_filter_by_category(self, authenticated_client, user):
        """Test filtering posts by category."""
        Post.objects.create(
            author=user,
            category=FeedCategory.NEWS,
            content='News post',
            is_published=True
        )
        Post.objects.create(
            author=user,
            category=FeedCategory.ALERT,
            content='Alert post',
            is_published=True
        )

        response = authenticated_client.get(
            '/api/v1/community-feed/posts/?category=news'
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    def test_get_post_detail(self, authenticated_client, post):
        """Test getting post detail."""
        response = authenticated_client.get(
            f'/api/v1/community-feed/posts/{post.id}/'
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data['content'] == post.content

    def test_update_own_post(self, authenticated_client, post):
        """Test updating own post."""
        response = authenticated_client.patch(
            f'/api/v1/community-feed/posts/{post.id}/',
            {'content': 'Updated content'}
        )

        assert response.status_code == status.HTTP_200_OK
        post.refresh_from_db()
        assert post.content == 'Updated content'

    def test_delete_own_post(self, authenticated_client, post):
        """Test deleting own post."""
        response = authenticated_client.delete(
            f'/api/v1/community-feed/posts/{post.id}/'
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        post.refresh_from_db()
        assert post.is_deleted is True

    def test_like_post(self, authenticated_client, other_user, post):
        """Test liking a post."""
        response = authenticated_client.post(
            f'/api/v1/community-feed/posts/{post.id}/like/'
        )

        assert response.status_code == status.HTTP_200_OK
        assert PostLike.objects.filter(post=post).count() == 1

    def test_like_post_duplicate(self, authenticated_client, post):
        """Test that liking twice doesn't create duplicate."""
        authenticated_client.post(
            f'/api/v1/community-feed/posts/{post.id}/like/'
        )
        response = authenticated_client.post(
            f'/api/v1/community-feed/posts/{post.id}/like/'
        )

        assert response.status_code == status.HTTP_200_OK
        # Still only one like
        assert PostLike.objects.filter(post=post).count() == 1

    def test_unlike_post(self, authenticated_client, post, user):
        """Test unliking a post."""
        PostLike.objects.create(post=post, user=user)

        response = authenticated_client.post(
            f'/api/v1/community-feed/posts/{post.id}/unlike/'
        )

        assert response.status_code == status.HTTP_200_OK
        assert PostLike.objects.filter(post=post).count() == 0

    def test_add_comment(self, authenticated_client, post):
        """Test adding a comment to post."""
        response = authenticated_client.post(
            '/api/v1/community-feed/comments/',
            {
                'post': str(post.id),
                'body': 'Great post!'
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert PostComment.objects.count() == 1

    def test_list_comments_for_post(self, authenticated_client, post, user):
        """Test listing comments for a post."""
        PostComment.objects.create(
            post=post,
            user=user,
            body='Great post!'
        )

        response = authenticated_client.get(
            f'/api/v1/community-feed/comments/?post={post.id}'
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    def test_delete_own_comment(self, authenticated_client, post, user):
        """Test deleting own comment."""
        comment = PostComment.objects.create(
            post=post,
            user=user,
            body='Comment to delete'
        )

        response = authenticated_client.delete(
            f'/api/v1/community-feed/comments/{comment.id}/'
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestPostModel:
    """Test suite for Post model."""

    def test_create_post_model(self, user):
        """Test creating a post model."""
        post = Post.objects.create(
            author=user,
            category=FeedCategory.NEWS,
            content='Test content'
        )

        assert post.author == user
        assert post.content == 'Test content'
        assert post.is_published is True

    def test_post_likes_count(self, user, other_user):
        """Test counting likes on post."""
        post = Post.objects.create(
            author=user,
            category=FeedCategory.NEWS,
            content='Test post'
        )

        PostLike.objects.create(post=post, user=user)
        PostLike.objects.create(post=post, user=other_user)

        assert post.likes.count() == 2

    def test_post_comments_count(self, user, other_user):
        """Test counting comments on post."""
        post = Post.objects.create(
            author=user,
            category=FeedCategory.NEWS,
            content='Test post'
        )

        PostComment.objects.create(post=post, user=user, body='Comment 1')
        PostComment.objects.create(post=post, user=other_user, body='Comment 2')

        assert post.comments.count() == 2
