# -*- coding: utf-8 -*-

""" 这个脚本的作用是用来处理连接 hive

@author: pu_yongjun
"""

from sqlalchemy.engine import create_engine


class HiveObj(object):
    """ 这个类的作用是用来执行操作 Hive
    """

    def __init__(self, host='127.0.0.1', port=10000, user='hdfs', database='default', *args, **kwargs):
        """ 这个函数的作用是用来初始化一些配置

        :param host: 地址
        :param port: 端口
        :return:
        """
        self.__host = host
        self.__port = port
        self.__user = user
        self.__database = database

    def __conn(self):
        """ 这个函数的作用是用来连接 Hive 数据库
        :return:
        """
        __engine = create_engine(
            'hive://{}@{}:{}/{}'.format(
                self.__user,
                self.__host,
                self.__port,
                self.__database
            ),
            connect_args={
                'configuration': {'hive.exec.reducers.max': '123'}
            },
        )
        return __engine

    def execute(self, hql):
        """ 这个函数的作用是用来执行 HQL 语句

        :param hql: 输入的 hql 语句
        :return:
        """
        back = self.__conn().execute(hql)
        return back.fetchall()
