from django.urls import path, include
from rest_framework.routers import DefaultRouter
from article.views import ArticleViewSet, UpdateArticleCategoryView
from comment.views import CommentViewSet
from rest_framework_nested.routers import NestedSimpleRouter

router = DefaultRouter()
router.register('articles', ArticleViewSet)

articles_router = NestedSimpleRouter(router, r'articles', lookup='article')

articles_router.register(
    r'comments',
    CommentViewSet,
    basename='article-comments'
)

articles_router.register(
    r'categories',
    UpdateArticleCategoryView,
    basename='article-categories'
)

app_name = 'article'

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(articles_router.urls)),
]
