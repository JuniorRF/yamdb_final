from api.v1.views import (CategoryViewSet, CommentViewSet, CustomUserViewSet,
                          GenreViewSet, ReviewViewSet, SignUpViewSet,
                          TitleViewSet, TokenViewSet)
from django.urls import include, path
from rest_framework import routers

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1_auth = routers.DefaultRouter()

router_v1_auth.register('signup', SignUpViewSet, basename='signup')
router_v1_auth.register('token', TokenViewSet, basename='token')
router_v1.register('users', CustomUserViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='viewsets'
)

router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('auth/', include(router_v1_auth.urls)),
    path('', include(router_v1.urls)),
]
