# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt

_author_ = 'luwt'
_date_ = '2023/3/13 11:43'


# 取出放置模板文件对象
def set_template_file_data(item, template_file_data):
    item.setData(Qt.UserRole, template_file_data)


def get_template_file_data(item):
    return item.data(Qt.UserRole)


# 取出放置方法体对象
def set_template_func_data(item, template_func):
    item.setData(Qt.UserRole, template_func)


def get_template_func_data(item):
    return item.data(Qt.UserRole)


# 取出放置导入异常数据的对象
def set_import_error_data(item, import_error_data):
    item.setData(Qt.UserRole, import_error_data)


def get_import_error_data(item):
    return item.data(Qt.UserRole)
