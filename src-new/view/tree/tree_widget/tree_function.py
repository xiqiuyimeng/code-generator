﻿# -*- coding: utf-8 -*-
"""
处理树节点相关操作
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem

from constant.constant import ADD_CONN_DIALOG_TITLE, EDIT_CONN_DIALOG_TITLE
from service.system_storage.conn_sqlite import SqlConnection
from service.system_storage.conn_type import get_conn_dialog
from view.dialog.conn import *

_author_ = 'luwt'
_date_ = '2020/7/6 11:34'


def make_sql_tree_item(parent, name, icon, sql_conn=None, checkbox=None):
    """
    构造树的子项
    :param parent: 要构造子项的父节点元素
    :param name: 构造的子节点名称
    :param icon: 图标，该元素的展示图标对象
    :param sql_conn: 构造的子节点隐藏属性，第一层连接层存放连接信息
    :param checkbox: 构造的子节点的复选框
    """
    item = QTreeWidgetItem(parent)
    item.setIcon(0, icon)
    item.setText(0, name)
    if sql_conn:
        # 隐藏属性，放入第一列
        item.setData(0, Qt.UserRole, sql_conn)
    if checkbox is not None:
        item.setCheckState(0, checkbox)
    # 在第二列放入是否正在打开的标识
    item.setData(1, Qt.UserRole, False)
    # 在第三列放入是否正在测试的标识
    item.setData(2, Qt.UserRole, False)
    return item


def add_conn_func(sql_type, tree_widget, screen_rect):
    """
    添加连接，打开弹窗，接收输入，保存系统库
    :param sql_type: 用来标识sql数据源类型
    :param tree_widget: 树对象
    :param screen_rect: 主窗口大小
    """
    conn_info = SqlConnection()
    show_conn_dialog(sql_type, tree_widget, conn_info, ADD_CONN_DIALOG_TITLE, screen_rect)


def edit_conn_func(sql_type, tree_widget, screen_rect, conn_info):
    show_conn_dialog(sql_type, tree_widget, conn_info, EDIT_CONN_DIALOG_TITLE, screen_rect)


def show_conn_dialog(sql_type, tree_widget, conn_info, title, screen_rect):
    """
    打开添加、编辑连接子窗口
    :param sql_type: 用来标识sql数据源类型
    :param tree_widget: 树对象
    :param conn_info: Connection对象，若该对象有id值，则认为操作为编辑操作，
        将在弹窗界面回显数据，若无数据，则为添加操作
    :param title: 弹窗的标题，与操作保持一致，不作为弹窗中回显数据标志，以conn_info为回显标志
    :param screen_rect: 主窗口大小
    """
    # 根据类型，动态获取对话框
    dialog = globals()[get_conn_dialog(sql_type)](conn_info, title, screen_rect, tree_widget.conn_name_dict)
    if title == ADD_CONN_DIALOG_TITLE:
        dialog.conn_changed.connect(lambda conn: add_conn_tree_item(tree_widget, conn))
    elif title == EDIT_CONN_DIALOG_TITLE:
        dialog.conn_changed.connect(lambda conn: update_conn_tree_item(tree_widget, conn))
    dialog.exec()


def add_conn_tree_item(tree_widget, connection):
    """
    添加树节点（连接），弹窗中点击确定后信号连接的槽函数，负责处理添加数据的操作
    :param tree_widget: 树对象
    :param connection: 弹窗中信号发射的连接对象，带有用户填写的信息
    """
    make_sql_tree_item(tree_widget, connection.name, tree_widget.conn_icon, connection)
    tree_widget.add_conn_name(connection.id, connection.name)


def update_conn_tree_item(tree_widget, connection):
    """
    更新树节点，弹窗中点击确定后信号连接的槽函数，负责处理编辑数据的操作
    :param tree_widget: 树对象
    :param connection: 弹窗中信号发射的连接对象，带有用户填写的信息
    """
    item = tree_widget.currentItem()
    item.setText(0, connection.name)
    item.setData(0, Qt.UserRole, connection)
    tree_widget.update_conn_name(connection.id, connection.name)


def make_sql_conn_tree_items(sql_conns, parent, icon):
    """
    根据本地保存的连接列表，构建树节点，在项目启动初始化时调用
    """
    for sql_conn in sql_conns:
        make_sql_tree_item(parent, sql_conn.conn_name, icon, sql_conn)


def make_db_items(tree_widget, parent_item, db_names):
    """构建数据库层叶子节点"""
    for db_name in db_names:
        make_sql_tree_item(parent_item, db_name, tree_widget.db_icon)


def make_table_items(tree_widget, parent_item, table_names):
    """构建数据表层叶子节点"""
    for table_name in table_names:
        make_sql_tree_item(parent_item, table_name, tree_widget.tb_icon, checkbox=Qt.Unchecked)


def check_table_status(parent):
    """
    检查表是否被全选，被部分选中，第三种情况为都没有选中
    :param parent: 在树部件中，表层次的父项，
    :return all_checked: 是否被全选
            parted_checked: 是否部分选中
    """
    all_checked, parted_checked = False, False
    # 如果数据库已经打开，再检测子项
    if parent.childCount():
        check_set = set()
        for index in range(parent.childCount()):
            # 将checkbox选中状态放入集合，状态有选中、部分选中与未选中，
            # 若集合元素为两个，则为部分选中，若为一个，取值判断。
            check_set.add(parent.child(index).checkState(0))
        if Qt.PartiallyChecked in check_set or len(check_set) > 1:
            parted_checked = True
        elif len(check_set) == 1 and check_set.pop() == Qt.Checked:
            all_checked = True
    return all_checked, parted_checked


def set_children_check_state(item, check_state):
    """
    将当前节点下所有项的复选框统一改为一个状态，并返回子元素名称列表
    :param item: 当前点击的树节点元素
    :param check_state: 复选框状态
    """
    children = list()
    for index in range(item.childCount()):
        child = item.child(index)
        child.setCheckState(0, check_state)
        children.append(child.text(0))
    return children
