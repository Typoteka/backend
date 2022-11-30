from rest_framework import viewsets, serializers

from core.models import (
    Article,
    Category,
    Comment,
)
from category.serializers import CategorySerializer
from user.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    owner = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'article_id', 'time', 'content', 'owner']
        read_only_fields = ['id', 'article_id']


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'date', 'preview', 'body', 'categories'
        ]
        read_only_fields = ['id']


class ArticleDetailSerializer(ArticleSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta(ArticleSerializer.Meta):
        fields = ArticleSerializer.Meta.fields + ['comments']



