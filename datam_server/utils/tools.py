#!/usr/share/app/anaconda3/bin/python3
# encoding: utf-8  

""" 
@version: v1.0 
@author: pu_yongjun
@license: Apache Licence
"""
import hashlib
import uuid
import xlwt


def handel_bool(value):
    """ 返回Python的 True 与 False
    :param value:
    :return:
    """
    if str(value).upper() == 'TRUE':
        return True
    return False


def gen_md5(str_con):
    """ 把输入的数据转换成MD5
    :param str_con: 输入的数据
    :return:
    """
    hl = hashlib.md5()
    hl.update(str(str_con).encode(encoding='utf-8'))
    return hl.hexdigest()


def primary_md5(type_id=None, *args, **kwargs):
    """ 这个方法是生成 uuid 的md5值

    :param type_id: 类型主要是uuid的类型
    type_id 是一个枚举值，主要还是uuid本身的类型，主要如下

       1、uuid1()——基于时间戳

               由MAC地址、当前时间戳、随机数生成。可以保证全球范围内的唯一性，
               但MAC的使用同时带来安全性问题，局域网中可以使用IP来代替MAC。

       2、uuid2()——基于分布式计算环境DCE（Python中没有这个函数）

                算法与uuid1相同，不同的是把时间戳的前4位置换为POSIX的UID。
                实际中很少用到该方法。

      3、uuid3()——基于名字的MD5散列值

                通过计算名字和命名空间的MD5散列值得到，保证了同一命名空间中不同名字的唯一性，
                和不同命名空间的唯一性，但同一命名空间的同一名字生成相同的uuid。

       4、uuid4()——基于随机数

                由伪随机数得到，有一定的重复概率，该概率可以计算出来。

       5、uuid5()——基于名字的SHA-1散列值

                算法与uuid3相同，不同的是使用 Secure Hash Algorithm 1 算法

    :param args: 一些uuid所需的值
    :param kwargs: 一些uuid所需的值
    :return: 返回一个uuid的md5值
    """
    uuid_dict = {
        1: uuid.uuid1,
        3: uuid.uuid3,
        4: uuid.uuid4,
        5: uuid.uuid5,
    }

    if type_id in uuid_dict.keys():
        if kwargs and (type_id in [3, 5]):
            name = kwargs.get('name')
            return gen_md5(uuid_dict.get(type_id)(uuid.NAMESPACE_DNS, name))
        else:
            return gen_md5(uuid_dict.get(type_id)())
    else:
        return gen_md5(uuid_dict.get(1)())


def array_split(arr, num):
    """ 这个函数的功能是把数组按照一定的长度切割成一些小数组

    :param arr: 原始数组
    :param num: 需要切割的长度
    :return:
    """
    return [arr[i: i + int(num)] for i in range(0, len(arr))]


def save_execl(data, path):
    """ 保存数据到execl
    :param data: 需要保存的数据，格式是 json 数组
    :param path: 需要保存的文件的路径
    :return:
    """
    # 新建一个excel对象
    wbk = xlwt.Workbook()
    # 添加一个名为 课程表的sheet页
    sheet = wbk.add_sheet('data')

    title = []
    data_list = [[]]
    table_width = 0

    for line_data in data:
        if isinstance(line_data, (dict,)):
            title = line_data.keys()
            table_width = len(list(line_data.values()))
            data_list.append(list(line_data.values()))
        else:
            return False

    for i in range(len(list(title))):  # 写入表头
        sheet.write(0, i, list(title)[i])  # 写入每行,第一个值是行，第二个值是列，第三个是写入的值

    for i in range(len(data_list)):
        if i != 0:  # 如果不是表头的话
            for j in range(table_width):
                sheet.write(i, j, data_list[i][j])  # 循环写入每行数据

    # 保存数据到‘test.xls’文件中
    wbk.save(path)
