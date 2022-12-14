from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from comment import serializers
from core.models import Comment
from core.permissions import IsOwner, IsStaff


# Create your views here.
class BaseCommentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = serializers.CommentSerializer
    queryset = Comment.objects.all()
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        permission_classes = []

        if self.action not in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsOwner | IsStaff]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super(BaseCommentViewSet, self).get_queryset()

        if self.kwargs.get('article_pk') is not None:
            queryset = queryset.filter(article_id=self.kwargs['article_pk'])

        return queryset.order_by('-time')


class CommentViewSetWithCreate(mixins.CreateModelMixin, BaseCommentViewSet):
    def perform_create(self, serializer):
        serializer.save(
            article_id=self.kwargs['article_pk'],
            owner=self.request.user
        )
