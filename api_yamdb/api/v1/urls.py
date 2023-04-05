from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryView,
    CommentViewSet,
    CustomUserViewSet,
    GenreView,
    ReviewViewSet,
    TitleView,
    api_registration,
    api_token_for_user,
)

router = DefaultRouter()
router.register('titles', TitleView, basename='titles')
router.register('categories', CategoryView, basename='categories')
router.register('genres', GenreView, 'genres')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)
router.register('users', CustomUserViewSet, basename='users')

auth_patterns = [
    path('signup/', api_registration, name='registration'),
    path('token/', api_token_for_user, name='token-for-user'),
]

urlpatterns = [
    path('auth/', include(auth_patterns)),
    path('', include(router.urls)),
]
