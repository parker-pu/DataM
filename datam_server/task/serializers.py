# Create your views here.
from rest_framework import serializers

from task.models import TaskModel, TaskEmailModel, EmailFile


class TaskModelSerializer(serializers.HyperlinkedModelSerializer):
    """ 任务信息
    """

    class Meta:
        model = TaskModel
        fields = (
            'id', 'name', 'describe', 'db_source', 'code_context',
            'task_status', 'insert_time', 'update_time'
        )


class TaskEmailModelSerializer(serializers.HyperlinkedModelSerializer):
    """ 任务信息
    """

    class Meta:
        model = TaskEmailModel
        fields = '__all__'


class EmailFileModelSerializer(serializers.HyperlinkedModelSerializer):
    """ 任务信息
    """

    class Meta:
        model = EmailFile
        fields = ('id', 'file_uuid', 'file_path', 'insert_time')
