from django.urls import path, include
from rest_framework.routers import DefaultRouter

from comment.views import CommentViewSet

router = DefaultRouter()
router.register('comments', CommentViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
]
