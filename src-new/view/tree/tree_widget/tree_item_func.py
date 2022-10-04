# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt

_author_ = 'luwt'
_date_ = '2022/10/1 17:55'


def get_item_sql_conn(item):
    return item.data(0, Qt.UserRole)


def set_item_sql_conn(item, sql_conn):
    # 隐藏第一列，放入连接信息
    item.setData(0, Qt.UserRole, sql_conn)


def get_item_conn_type(item):
    return item.data(1, Qt.UserRole)


def set_item_conn_type(item, conn_type):
    # 在第二列放入连接类型
    item.setData(1, Qt.UserRole, conn_type)


def get_item_opening_flag(item):
    return item.data(2, Qt.UserRole)


def set_item_opening_flag(item, opening_flag):
    # 在第三列放入是否正在打开的标识
    item.setData(2, Qt.UserRole, opening_flag)


def get_item_testing_flag(item):
    return item.data(3, Qt.UserRole)


def set_item_testing_flag(item, testing_flag):
    # 在第四列放入是否正在测试的标识
    item.setData(3, Qt.UserRole, testing_flag)


def get_item_opening_worker(item):
    return item.data(4, Qt.UserRole)


def set_item_opening_worker(item, opening_worker):
    # 在第五列放入正在打开节点的线程
    item.setData(4, Qt.UserRole, opening_worker)


def get_item_testing_worker(item):
    return item.data(5, Qt.UserRole)


def set_item_testing_worker(item, testing_worker):
    # 第六列放入正在测试网络连接的线程
    item.setData(5, Qt.UserRole, testing_worker)


def set_item_opened_record(item, opened_item_record):
    # 放入历史记录表中的记录
    item.setData(6, Qt.UserRole, opened_item_record)


def get_item_opened_record(item):
    return item.data(6, Qt.UserRole)
