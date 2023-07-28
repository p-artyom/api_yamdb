from django.urls import include, path
from rest_framework import routers

from api.views import (
    APIGetToken,
    APISignup,
    CategoryCreateListDestroyViewSet,
    CommentViewSet,
    GenreCreateListDestroyViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
)

v1_router = routers.DefaultRouter()
v1_router.register(
    'categories',
    CategoryCreateListDestroyViewSet,
    basename='categories',
)
v1_router.register(
    'genres',
    GenreCreateListDestroyViewSet,
    basename='genres',
)
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='api',
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='api',
)
v1_router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
]
