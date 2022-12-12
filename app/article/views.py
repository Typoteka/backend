from article import serializers
from core.models import (
    Article,
    Category,
    Comment,
)
from core.permissions import IsStaff, IsOwner
from django.db.models import Count
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
)
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'best_first',
                OpenApiTypes.INT, enum=[0, 1],
                description='Articles with the most comments go first',
            ),
        ]
    )
)
class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ArticleSerializer
    queryset = Article.objects.all()
    authentication_classes = [TokenAuthentication]
    filter_backends = (SearchFilter,)
    search_fields = ['title', 'preview', 'body']

    def get_queryset(self):
        queryset = super(ArticleViewSet, self).get_queryset()
        best_first = bool(int(self.request.query_params.get('best_first', 0)))

        if best_first:
            queryset = queryset.annotate(
                num_comments=Count('comments')
            ).order_by('-num_comments')

        return queryset

    def get_permissions(self):
        permission_classes = []

        if self.action not in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsStaff]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        match self.action:
            case 'retrieve':
                return serializers.ArticleDetailSerializer
            case 'upload_image':
                return serializers.ArticleImageSerializer

        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to article."""
        article = self.get_object()
        serializer = self.get_serializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateArticleCategoryView(ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsStaff]

    @classmethod
    def _get_or_404(cls, class_, pk):
        try:
            obj = class_.objects.get(pk=pk)
        except class_.DoesNotExist:
            raise NotFound(
                detail=f'{class_.__name__} with id {pk} does not exist',
                code=404
            )

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
