# -*- coding: utf-8 -*-
from view.tree.tree_function import add_conn_func

_author_ = 'luwt'
_date_ = '2022/5/29 16:51'


def open_conn_dialog(tree_widget, screen_rect):
    """
    打开添加、编辑连接子窗口
    :param tree_widget: 树对象
    :param screen_rect: 父窗口大小
    """
    add_conn_func(tree_widget, screen_rect)
