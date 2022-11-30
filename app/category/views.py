from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from category.serializers import CategorySerializer
from core.models import Category
from core.permissions import IsStaff


# Create your views here.
class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        permission_classes = []

        if self.action not in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsStaff]

        return [permission() for permission in permission_classes]

