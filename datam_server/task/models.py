from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from user.models import DBSourceModel


class TaskModel(models.Model):
    """ 任务信息
    """
    name = models.CharField(max_length=255, verbose_name="任务名")
    describe = models.TextField(verbose_name="任务描述")
    db_source = models.ForeignKey(
        DBSourceModel,
        related_name='db_source',
        on_delete=models.CASCADE,
        default='',
        verbose_name='源数据库'
    )
    code_context = models.TextField(verbose_name="代码内容")
    task_status = models.BooleanField(verbose_name="任务状态", default=True)
    insert_time = models.DateTimeField(auto_now=True, verbose_name="插入时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = 'task'  # 指定表名


class TaskEmailModel(models.Model):
    """ 一个任务对应多个邮件用户
    """
    task_uuid = models.CharField(max_length=50, verbose_name="执行任务的唯一id")
    task = models.ForeignKey(
        TaskModel,
        related_name='task',
        on_delete=models.CASCADE,
        default='',
        verbose_name="task 外键",
    )
    user = models.ForeignKey(
        User,
        related_name='user',
        on_delete=models.CASCADE,
        default='',
        verbose_name="执行用户",
    )
    insert_time = models.DateTimeField(auto_now=True, verbose_name="插入时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = 'task_email'  # 指定表名


class EmailFile(models.Model):
    """ 发送到的邮件的列表
    """
    file_uuid = models.CharField(max_length=50, verbose_name="文件id")
    task_email = models.ForeignKey(
        TaskEmailModel,
        related_name='task_email',
        on_delete=models.CASCADE,
        default='',
        verbose_name="TaskEmailModel 外键",
    )
    file_path = models.TextField(verbose_name="文件路径")
    insert_time = models.DateTimeField(auto_now=True, verbose_name="插入时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = 'email_file'  # 指定表名
