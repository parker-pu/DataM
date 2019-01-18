# encoding: utf-8

"""
@version: v1.0
@author: pu_yongjun
@license: Apache Licence

这个脚本的作用是用来处理一些周期性任务（定时）任务的 Django 的视图
"""
from rest_framework import viewsets
from rest_framework.response import Response

from custom.permission import CustomPermission
from django_celery_beat.models import PeriodicTask

from task.periodic.serializers import PeriodicTaskSerializer


class PeriodicTaskViewSet(viewsets.ModelViewSet):
    """ 查看定时器
    """
    permission_classes = (CustomPermission,)  # 设置权限
    queryset = PeriodicTask.objects.order_by('-id').all()
    serializer_class = PeriodicTaskSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        # 数据进行重新封装，把用户信息与UUID给取出来
        # 为什么不重写 PeriodicTask 这个 Model ,因为这个模型 name 字段是唯一值
        handel_data = serializer.data
        result_data = []
        for line in handel_data:
            # 判断任务名中是否是有 ## 存在
            name = line.get("name")
            if "##" in name:
                line["uuid"] = str(name).split("##")[0]
                line["name"] = str(name).split("##")[1]

            # 修改定时的配置
            line["cron"] = "{} {} {} {} {}".format(
                line.get("minute"),
                line.get("hour"),
                line.get("day_of_week"),
                line.get("day_of_month"),
                line.get("month_of_year")
            )
            result_data.append(line)
        return Response(result_data)
