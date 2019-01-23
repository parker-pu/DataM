"""datam_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, re_path, include
from rest_framework import routers

from datam_server import settings
from my_token.views import (
    UserViewSet,
    AuthTokenView,
    DBSourceViewSet
)
from django.conf.urls import static

from task.periodic.views import PeriodicTaskViewSet
from task.views import (
    TaskViewSet,
    ExecTaskViewSet,
    TaskEmailViewSet,
    TaskLogViewSet, FileViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', UserViewSet)
router_v1.register(r'db_source', DBSourceViewSet)
router_v1.register(r'task', TaskViewSet)
router_v1.register(r'task_emxail', TaskEmailViewSet)
router_v1.register(r'periodic-task', PeriodicTaskViewSet)


def index(request, url=None):
    """ 这个函数的作用是返回 VUE 生成的主页
    """
    return render(request, 'dist/index.html')


urlpatterns = [
    re_path('^$', index),  # 首页
    path('<str:url>', index),  # 首页
    path('admin/', admin.site.urls),  # Django 后台
    path('api/v1/', include(router_v1.urls)),  # 相应的接口
    path('api/v1/exec_task/', ExecTaskViewSet.as_view(
        actions={
            'post': 'post'
        }
    )),  # 执行任务相应的接口
    re_path('api/v1/task_log/(?P<task_id>.*)$', TaskLogViewSet.as_view(
        actions={
            'get': 'list',
            'delete': 'delete'
        }
    )),  # 查看任务执行状况的接口
    re_path('api/v1/file/(?P<file_id>.*)$', FileViewSet.as_view(
        actions={
            'get': 'list',
            'delete': 'delete'
        }
    )),  # 获取发送邮件的附件的信息

    path('api-token-auth/', AuthTokenView.as_view()),  # token 认证

    re_path('static/(?P<path>.*)$', static.serve,
            {'document_root': settings.STATIC_ROOT}, name='static'),
]
