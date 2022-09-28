# -*- coding: utf-8 -*-
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from service.system_storage.conn_type import ConnTypeEnum
from view.tree.tree_widget.tree_function import add_conn_func

_author_ = 'luwt'
_date_ = '2022/5/29 16:51'


def open_conn_dialog(sql_type, tree_widget, screen_rect):
    """
    打开添加、编辑连接子窗口
    :param sql_type: 用来标识sql数据源类型
    :param tree_widget: 树对象
    :param screen_rect: 父窗口大小
    """
    add_conn_func(sql_type, tree_widget, screen_rect)


def add_datasource_action(main_window, parent, action_name, action_icon_path):
    """添加数据源action"""
    add_action = QAction(QIcon(action_icon_path), action_name, main_window)
    add_action.setStatusTip('在左侧列表中添加一条连接')
    add_action.triggered.connect(lambda: open_conn_dialog(action_name, main_window.tree_widget, main_window.geometry()))
    parent.addAction(add_action)


def add_sql_datasource_actions(main_window, parent):
    """添加sql数据源action"""
    for conn_type in ConnTypeEnum:
        add_datasource_action(main_window, parent, conn_type.value.display_name, conn_type.value.type_icon)
