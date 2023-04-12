import json
import logging

from django.http import JsonResponse
from drf_haystack.filters import HaystackFilter
from drf_haystack.viewsets import HaystackViewSet
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from app.consumers import ChatConsumer, PENDING
from app.models import User, Article
from app.serializers import UserCreateSerializer, LoginSerializer, UserListSerializer, ArticleIndexSerializer
from utils.pagination import StandardPagination
from drf_gather.mqtt import client as mqtt_client

logger = logging.getLogger(__name__)


class UserCreateAPI(generics.CreateAPIView):
    authentication_classes = []
    serializer_class = UserCreateSerializer


class UserLoginAPI(APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        user = LoginSerializer(data=request.data)
        user.is_valid(raise_exception=True)

        # 实现方式一：
        for item in PENDING.get('room1'):
            item.send('test')

        # 实现方式二：
        # ChatConsumer.group_send('room1', 'wzj')

        return Response({
            'username': user.user.username,
            'token': user.token
        })


class UserListAPI(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    pagination_class = StandardPagination


class ArticleSearchView(HaystackViewSet):
    index_models = [Article]
    serializer_class = ArticleIndexSerializer
    pagination_class = StandardPagination
    authentication_classes = []

    # def list(self, request, *args, **kwargs):
    #     res = super(ArticleSearchView, self).list(self, request, *args, **kwargs)
    #     return Response(res.data)


def publish_message(request):
    request_data = json.loads(request.body)
    rc, mid = mqtt_client.publish(request_data['topic'], request_data['msg'])
    return JsonResponse({'code': rc})
