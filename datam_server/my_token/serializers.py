# Create your views here.
from django.contrib.auth.models import User
from rest_framework import serializers

from my_token.models import DBSourceModel


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """用户的配置信息
    """

    class Meta:
        model = User
        fields = "__all__"


class DBSourceSerializer(serializers.HyperlinkedModelSerializer):
    """ 数据库类型
    """

    class Meta:
        model = DBSourceModel
        fields = (
            'id', 'db_type', 'describe', 'host',
            'port', 'database', 'user', 'password'
        )
