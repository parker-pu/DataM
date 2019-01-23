from django.db import models


# Create your models here.


class DBSourceModel(models.Model):
    """ 源数据库配置
    """
    db_type = models.CharField(max_length=100, verbose_name="数据库类型名")
    describe = models.TextField(verbose_name="数据库类型描述")
    host = models.CharField(max_length=100, verbose_name="数据库地址")
    port = models.IntegerField(verbose_name="数据库端口")
    database = models.CharField(max_length=200, verbose_name="数据库")
    user = models.CharField(max_length=10, verbose_name="数据库用户名")
    password = models.CharField(max_length=24, verbose_name="数据库密码")
    insert_time = models.DateTimeField(auto_now=True, verbose_name="插入时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = 'db_source'  # 数据库源配置
