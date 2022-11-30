from django.shortcuts import render
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from category.serializers import CategorySerializer
from core.models import Category
from core.permissions import IsStaff


# Create your views here.
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'with_assigned_articles',
                OpenApiTypes.INT, enum=[0, 1],
                description='Articles with the biggest amount of comments go first',
            ),
        ]
    )
)
class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        queryset = self.queryset
        with_assigned_articles = bool(int(self.request.query_params.get('with_assigned_articles', 0)))

        if with_assigned_articles:
            queryset = queryset.filter(article__isnull=False).distinct()

        return queryset

    def get_permissions(self):
        permission_classes = []

        if self.action not in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsStaff]

        return [permission() for permission in permission_classes]

