# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt

_author_ = 'luwt'
_date_ = '2022/10/1 17:55'


def get_item_sql_conn(item):
    return item.data(0, Qt.UserRole)


def set_item_sql_conn(item, sql_conn):
    # 第二列，放入连接信息
    item.setData(0, Qt.UserRole, sql_conn)


def get_item_conn_type(item):
    return item.data(1, Qt.UserRole)


def set_item_conn_type(item, conn_type):
    # 在第三列放入连接类型
    item.setData(1, Qt.UserRole, conn_type)


def set_item_opened_record(item, opened_item_record):
    # 放入历史记录表中的记录
    item.setData(2, Qt.UserRole, opened_item_record)


def get_item_opened_record(item):
    return item.data(2, Qt.UserRole)


def set_item_opened_tab(item, tab_widget):
    # 放入打开的tab_widget
    item.setData(3, Qt.UserRole, tab_widget)


def get_item_opened_tab(item):
    return item.data(3, Qt.UserRole)
