from category.serializers import CategorySerializer
from core.models import (
    Article,
    Comment,
)
from rest_framework import serializers

from comment.serializers import CommentSerializer




class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'date', 'preview', 'body', 'cover', 'categories'
        ]
        read_only_fields = ['id', 'cover']


class ArticleDetailSerializer(ArticleSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta(ArticleSerializer.Meta):
        fields = ArticleSerializer.Meta.fields + ['comments']


class ArticleImageSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(
        max_length=None,
        allow_empty_file=True,
        allow_null=True,
        required=False
    )

    class Meta:
        model = Article
        fields = ('id', 'cover')
        read_only_fields = ('id',)
