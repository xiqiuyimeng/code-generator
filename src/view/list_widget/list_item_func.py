# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt

_author_ = 'luwt'
_date_ = '2023/3/13 11:43'


def set_template_file_data(item, template_file_data):
    item.setData(Qt.UserRole, template_file_data)


def get_template_file_data(item):
    return item.data(Qt.UserRole)
