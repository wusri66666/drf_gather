from django.urls import path
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework import routers

from app.apis import UserCreateAPI, UserLoginAPI, UserListAPI, ArticleSearchView, publish_message

router = routers.DefaultRouter()
router.register("article/search", ArticleSearchView, basename="article-search")

urlpatterns = [
    path('register/', UserCreateAPI.as_view()),
    path('login/', UserLoginAPI.as_view()),
    path('refresh/', refresh_jwt_token),
    path('user/', UserListAPI.as_view()),
    path('publish/', publish_message, name='publish'),
]

urlpatterns += router.urls
