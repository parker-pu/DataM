# Create your views here.
# encoding: utf-8
import os

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from user.models import DBSourceModel
from task.tasks import now_exec_task, schedule_task
from django_celery_results.models import TaskResult as CeleryTaskResult
from custom.permission import CustomPermission
from task.models import (
    TaskModel,
    TaskEmailModel, EmailFile)
from task.serializers import (
    TaskModelSerializer,
    TaskEmailModelSerializer, EmailFileModelSerializer
)
from utils.tools import handel_bool


class TaskViewSet(viewsets.ModelViewSet):
    """ 任务配置信息
    """
    permission_classes = (CustomPermission,)  # 设置权限

    queryset = TaskModel.objects.all()
    serializer_class = TaskModelSerializer

    def list(self, request, *args, **kwargs):
        """ 获取所有任务
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        back_data = []
        for line in queryset:
            new_line = line.__dict__
            new_line['db_source'] = line.db_source.host
            del new_line['_state']
            back_data.append(new_line)
        return Response(back_data)

    def update(self, request, *args, **kwargs):
        """ 这个函数的作用是改写更新task
        """
        instance = self.get_object()
        handel_data = request.data
        db_source = DBSourceModel.objects.filter(id=handel_data.get('db_source_id')).first()

        # 更新相应的任务
        TaskModel.objects.filter(id=handel_data.get('id')).update(
            name=handel_data.get('name'),
            describe=handel_data.get('describe'),
            db_source=db_source,
            code_context=handel_data.get('code_context'),
            task_status=handel_bool(handel_data.get('task_status', 'False')),
        )

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        headers = self.get_success_headers(request.data)
        return Response(
            {"task_id": handel_data.get('id')},
            status=status.HTTP_201_CREATED, headers=headers
        )

    def create(self, request, *args, **kwargs):
        """ 创建任务配置
        """
        handel_data = request.data
        db_source = DBSourceModel.objects.filter(id=handel_data.get('db_source_id')).first()

        tm = TaskModel.objects.create(
            name=handel_data.get('name'),
            describe=handel_data.get('describe'),
            db_source=db_source,
            code_context=handel_data.get('code_context'),
            task_status=handel_bool(handel_data.get('task_status', 'False')),
        )

        headers = self.get_success_headers(request.data)
        return Response({"task_id": tm.id}, status=status.HTTP_201_CREATED, headers=headers)


class TaskEmailViewSet(ReadOnlyModelViewSet):
    """ 任务日志
    """
    permission_classes = (CustomPermission,)  # 设置权限

    queryset = TaskEmailModel.objects.all()
    serializer_class = TaskEmailModelSerializer


class ExecTaskViewSet(viewsets.ModelViewSet):
    """ 立即执行 task
    """
    permission_classes = (CustomPermission,)  # 设置权限

    @staticmethod
    def post(request, *args, **kwargs):
        """ 通过Post方法异步返回task的结果
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        handel_data = request.data
        # 判断必填数据是否完整
        if not (handel_data.get('task_id') and handel_data.get('user_list')):
            return Response(
                data={"message": "任务名与用户不能为空", "detailed": "输入不完整"},
                status=400
            )

        # 判断使用 celery 来执行
        if not handel_data.get('cron_data'):
            exec_task_id = now_exec_task.delay(request.data)
        else:
            exec_task_id = schedule_task.delay(request.data)
        return Response(
            data={"message": "任务调度成功", "detailed": "", "exec_task_id": str(exec_task_id)},
            status=200
        )


class TaskLogViewSet(viewsets.ModelViewSet):
    """ 立即执行 task
    """
    permission_classes = (CustomPermission,)  # 设置权限

    def list(self, request, *args, **kwargs):
        """ 通过GET方法返回 task 日志的结果
        :return:
        """
        result = []
        celery_task_result = CeleryTaskResult \
            .objects \
            .values("id", "task_id", "traceback", "status", "date_done") \
            .order_by('-id') \
            .all()
        # .filter(task_name='task.tasks.now_exec_task') \

        for line in celery_task_result:
            _tem = TaskEmailModel.objects.filter(task_uuid=line.get("task_id")).first()
            if not _tem:
                continue
            line['task_uuid'] = line.get("task_id")
            del line['task_id']
            line['task_name'] = _tem.task.name
            line['task_describe'] = _tem.task.describe
            line['username'] = _tem.user.username
            result.append(line)

        headers = self.get_success_headers(request.data)
        return Response(
            data=result,
            status=200,
            headers=headers
        )

    def delete(self, request, task_id, *args, **kwargs):
        """ 这个函数的作用是用来删除日志
        """
        CeleryTaskResult.objects.filter(id=task_id).delete()
        headers = self.get_success_headers(request.data)
        return Response({"id": task_id}, status=status.HTTP_201_CREATED, headers=headers)


class FileViewSet(viewsets.ModelViewSet):
    """ 立即执行 task
    """
    permission_classes = (CustomPermission,)  # 设置权限
    queryset = EmailFile.objects.order_by('-id').all()
    serializer_class = EmailFileModelSerializer

    def list(self, request, *args, **kwargs):
        """ 这个函数的作用是用来获取发送邮件的附件的信息
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # return self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)

        result = []

        for line in serializer.data:
            new_ef_obj = EmailFile.objects.filter(id=line.get('id')).first()
            line['file_path'] = line.get('file_path')
            line['task_uuid'] = new_ef_obj.task_email.task_uuid
            line['task_name'] = new_ef_obj.task_email.task.name
            line['task_describe'] = new_ef_obj.task_email.task.describe
            line['username'] = new_ef_obj.task_email.user.username
            result.append(line)

        headers = self.get_success_headers(request.data)
        return Response(
            data=result,
            status=200,
            headers=headers
        )

    def delete(self, request, file_id, *args, **kwargs):
        """ 这个函数的作用是用来删除文件
        (1)找出与删除数据库中的文件存储的数据
        (2)删除本地文件数据
        """
        efj = EmailFile.objects.filter(id=file_id)
        file_path = efj.first().file_path
        os.remove(file_path)
        efj.delete()  # 删除数据库源数据
        headers = self.get_success_headers(request.data)
        return Response({"id": file_id}, status=status.HTTP_201_CREATED, headers=headers)
