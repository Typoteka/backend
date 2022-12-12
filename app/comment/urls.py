from django.urls import path, include
from rest_framework.routers import DefaultRouter

from comment.views import BaseCommentViewSet

router = DefaultRouter()
router.register('comments', BaseCommentViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
]
