# -*- coding: utf-8 -*-

""" 这个脚本的作用是用来处理连接 MySQL

此版本没有考虑发送失败的问题

@author: pu_yongjun
"""

import threading

from sqlalchemy import create_engine


class MySQLObj(object):
    """ 这个类的作用是用来处理 MySQL 的数据
    """
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """ 通过单例模式来减少对数据库的操作

        :param args:
        :param kwargs:
        :return:
        """
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, host, port, database, user, password, *args, **kwargs):
        """ 这个函数的作用是初始化一些参数

        :param host:
        :param port:
        :param database:
        :param user:
        :param password:
        """
        self.__mysql_host = host
        self.__mysql_port = port
        self.__mysql_database = database
        self.__mysql_user = user
        self.__mysql_password = password

    def __conn(self):
        """ 这个函数的作用是返回数据库的连接

        :return:
        """
        engine = create_engine(
            "mysql+pymysql://{}:{}@{}:{}/{}".format(
                self.__mysql_user,
                self.__mysql_password,
                self.__mysql_host,
                self.__mysql_port,
                self.__mysql_database
            ),
            max_overflow=5,
            encoding="utf-8",
            echo_pool=True
        )

        return engine.connect()

    def execute(self, sql):
        """ 这个函数的作用是执行 SQL 语句

        :param sql:
        :return:
        """
        with self.__conn() as con:
            return con.execute(sql).fetchall()
