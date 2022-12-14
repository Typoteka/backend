from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from core.models import Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id']
