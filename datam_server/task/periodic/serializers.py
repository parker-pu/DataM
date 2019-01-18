# Create your views here.
# encoding: utf-8
from django_celery_beat.models import PeriodicTask
from rest_framework import serializers


class PeriodicTaskSerializer(serializers.HyperlinkedModelSerializer):
    """ 定时器序列化
    """
    # crontab 对应的外键表
    minute = serializers.CharField(source='crontab.minute')
    hour = serializers.CharField(source='crontab.hour')
    day_of_week = serializers.CharField(source='crontab.day_of_week')
    day_of_month = serializers.CharField(source='crontab.day_of_month')
    month_of_year = serializers.CharField(source='crontab.month_of_year')

    class Meta:
        model = PeriodicTask
        fields = (
            'id', 'name', 'task', 'args', 'kwargs', 'date_changed',
            'description', 'enabled', 'total_run_count',
            'minute', 'hour', 'day_of_week', 'day_of_month', 'month_of_year'
        )
