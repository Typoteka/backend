from rest_framework import serializers

from core.models import Comment
from user.serializers import UserSerializer

from core.models import Article


class ArticleCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title']
        read_only_fields = ['id', 'title']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    owner = UserSerializer(read_only=True)
    article = ArticleCommentSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'article', 'time', 'content', 'owner']
        read_only_fields = ['id', 'article']
