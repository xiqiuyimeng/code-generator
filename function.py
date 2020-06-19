# -*- coding: utf-8 -*-
from db_info import *
_author_ = 'luwt'
_date_ = '2020/6/15 15:21'


conn_info = 'centos121', 'root', 'admin', 3306
executor = DBExecutor(*conn_info)


def get_dbs():
    """获取链接下所有的库"""
    return executor.get_dbs()


def switch_db(db):
    """切换库"""
    executor.switch_db(db)


def get_tables():
    """获取库下所有的数据库表"""
    return executor.get_tables()


def get_cols(table):
    """获取表下所有的字段名"""
    return executor.get_cols(table)


def close():
    executor.exit()
