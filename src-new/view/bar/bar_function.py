# -*- coding: utf-8 -*-
from view.tree.tree_widget.tree_function import add_conn_func

_author_ = 'luwt'
_date_ = '2022/5/29 16:51'


def open_conn_dialog(sql_type_action, tree_widget, screen_rect):
    """
    打开添加、编辑连接子窗口
    :param sql_type_action: 用来标识sql数据源类型
    :param tree_widget: 树对象
    :param screen_rect: 父窗口大小
    """
    add_conn_func(sql_type_action.text(), tree_widget, screen_rect)

