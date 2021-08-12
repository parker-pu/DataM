# encoding: utf-8

"""
@version: v1.0
@author: pu_yongjun
@license: Apache Licence

这个模块下的文件的作用是用来定义一些 task 任务
"""
import json

import pytz
from django.contrib.auth.models import User

from datam_server.settings import CELERY_TIMEZONE
from db.hive2_obj import HiveObj
from db.mysql_obj import MySQLObj
from task.models import TaskModel, TaskEmailModel, EmailFile
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from celery import shared_task
from celery._state import get_current_task
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from utils.tools import save_execl, primary_md5


def send_mail(subject, content, email_list, attach_file=None):
    """ 这个函数的作用是用来发送邮件
    :param subject: 主题
    :param content: 内容
    :param email_list: 邮件列表
    :param attach_file: 附件
    :return:
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    msg = EmailMultiAlternatives(subject, content, from_email, email_list)
    if attach_file:
        msg.attach_file(attach_file)  # 添加附件（可选）
    msg.send()  # 发送


class DBSelect:
    """ 这个类的作用就是用来执行任务
    """

    def __init__(self, **kwargs):
        """ 初始化数据库选择的信息
        :param kwargs:
        """
        db_type = str(kwargs.get('db_type')).upper()
        if db_type == 'MYSQL':
            self.__ini_cls = MySQLObj(**kwargs)
        elif db_type == 'HIVE':
            self.__ini_cls = HiveObj(**kwargs)

    def exec(self, sql):
        back_data = self.__ini_cls.execute(sql)
        data = [dict(zip(result.keys(), result)) for result in back_data]
        return data


@shared_task
def save_task_user(data, task_uuid):
    """ 保存每个配置的任务对应的用户
    """
    task_obj = TaskModel.objects.filter(id=data.get("task_id")).first()
    for user_id in data.get("user_list"):
        user = User.objects.filter(id=user_id).first()
        TaskEmailModel.objects.create(
            task_uuid=task_uuid,
            user=user,
            task=task_obj
        )
    return True


@shared_task
def exec_task(data, task_uuid):
    """ 执行相应任务

    步骤:
    (1)获取所需要执行任务的信息
    (2)获取所需要发送邮件的用户
    (3)把信息传递给相应的执行函数
    """
    task_obj = TaskModel.objects.filter(id=data.get("task_id")).first()

    # 获取 email 列表
    task_email_model_obj = TaskEmailModel.objects.filter(task_uuid=task_uuid)
    email_list = []
    for email in task_email_model_obj.all():
        email_list.append(email.user.email)

    # 获取数据源
    db_source = task_obj.db_source.__dict__
    del db_source['_state']

    # 执行对应的SQL语句
    db = DBSelect(**db_source)
    back_data = db.exec(sql=task_obj.code_context)

    # 把数据打包成 execl , 以任务名称作为文件名
    file_uuid = primary_md5()
    path = 'static/data/{}.xls'.format(str(file_uuid))
    save_execl(data=back_data, path=path)

    # 把文件信息保存到数据库中
    EmailFile.objects.create(
        file_uuid=file_uuid,
        task_email=task_email_model_obj.first(),
        file_path=path
    )

    # 发送邮件
    send_mail(
        subject=task_obj.name,
        content=task_obj.describe,
        email_list=email_list,
        attach_file=path
    )
    return True


@shared_task
def schedule_task(data):
    """ 这个函数的作用是根据定时任务去完成定时任务的配置
    :param data: 前端提交上来的数据
    :return:
    """
    # 获取任务的id
    task_uuid = get_current_task().request.id

    # 配置定时任务
    cron_data = data.get('cron_data', {})
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute=cron_data.get('minute', '*'),
        hour=cron_data.get('hour', '*'),
        day_of_week=cron_data.get('day_of_week', '*'),
        day_of_month=cron_data.get('day_of_month', '*'),
        month_of_year=cron_data.get('month_of_year', '*'),
        timezone=pytz.timezone(CELERY_TIMEZONE)
    )
    # 配置任务的一些信息
    # (1)获取任务名称
    # (1)配置所需要接收的参数
    task_obj = TaskModel.objects.filter(id=data.get("task_id")).first()
    PeriodicTask.objects.create(
        crontab=schedule,
        name="{}##{}".format(task_uuid, task_obj.name),
        task='task.tasks.now_exec_task',
        kwargs=json.dumps({"data": data}),
        description=task_obj.describe
    )

    return True


@shared_task
def now_exec_task(data, *args, **kwargs):
    """ 这个函数的作用是用来立即执行同步任务

    步骤
    （1）取到 task 的信息
    （2）根据 task.id 取到需要发送邮件的用户信息
    :param data:
    :return:
    """
    print(kwargs)
    # 获取任务的id
    task_uuid = get_current_task().request.id

    # 保存任务对应的需要发送的用户
    save_task_user.delay(data=data, task_uuid=task_uuid)

    # 执行相应任务
    exec_task.delay(data=data, task_uuid=task_uuid)
    return True
