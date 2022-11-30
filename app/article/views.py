from article import serializers
from core.models import (
    Article,
    Category,
    Comment,
)
from core.permissions import IsStaff, IsOwner
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


# Create your views here.
class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ArticleSerializer
    queryset = Article.objects.all()
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        permission_classes = []

        if self.action not in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsStaff]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.ArticleDetailSerializer

        return self.serializer_class


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    queryset = Comment.objects.all()
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        permission_classes = []

        if self.action not in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsOwner]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Comment.objects.filter(article=self.kwargs['article_pk'])

    def perform_create(self, serializer):
        serializer.save(article_id=self.kwargs['article_pk'], owner=self.request.user)


class UpdateArticleCategoryView(ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsStaff]

    @classmethod
    def _get_or_404(cls, class_, pk):
        try:
            obj = class_.objects.get(pk=pk)
        except class_.DoesNotExist:
            raise NotFound(detail=f'{class_.__name__} with id {pk} does not exist', code=404)

        return obj

    def update(self, _request, pk=None, article_pk=None):
        article = self._get_or_404(Article, article_pk)
        category = self._get_or_404(Category, pk)

        article.categories.add(category)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, _request, pk=None, article_pk=None):
        article = self._get_or_404(Article, article_pk)
        category = self._get_or_404(Category, pk)

        article.categories.remove(category)

        return Response(status=status.HTTP_204_NO_CONTENT)

