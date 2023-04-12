from django.db.models import Q
from drf_haystack.serializers import HaystackSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from app.models import User
from app.search_indexes import ArticleIndex


class UserCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create(
            phone=validated_data.get('phone'),
            username=validated_data.get('username')
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    class Meta:
        model = User
        fields = ['phone', 'username', 'password']


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, attrs):
        user = self._many_method_login(**attrs)

        # 通过user对象生成payload载荷
        payload = jwt_payload_handler(user)
        # 通过payload签发token
        token = jwt_encode_handler(payload)

        # 将user和token存放在序列化对象中,方便返回到前端去
        self.user = user
        self.token = token

        return attrs

    # 多方式登录
    def _many_method_login(self, **attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = User.objects.filter(Q(phone=username) | Q(username=username))

        if not user:
            raise ValidationError({'username': '账号有误'})

        if not user.first().check_password(password):
            raise ValidationError({'password': '密码错误'})

        return user.first()


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ArticleIndexSerializer(HaystackSerializer):
    test1 = serializers.SerializerMethodField()

    def get_test1(self, obj):
        return obj.id

    class Meta:
        index_classes = [ArticleIndex]  # 索引类的名称
        fields = ('text', "id", "title", "content", "author", "count", "test1")