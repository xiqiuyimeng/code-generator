# -*- coding: utf-8 -*-
"""
处理主窗口对象相关功能
"""
from table_func import *
from PyQt5.QtWidgets import QTreeWidgetItem
from db_info import DBExecutor
from sys_info_storage.sqlite import Connection
from constant import ADD_CONN_MENU, EDIT_CONN_MENU
from conn_dialog import Ui_Dialog
_author_ = 'luwt'
_date_ = '2020/7/2 15:57'


def open_connection(gui, conn_id):
    """根据连接名称，从当前维护的连接字典中获取一个数据库连接操作对象"""
    # 如果该连接已经打开，直接取，否则获取新的连接
    if not gui.connected_dict.get(conn_id):
        # id name host port user pwd
        conn_info = gui.conns_dict.get(conn_id)
        executor = DBExecutor(*conn_info[2:])
        gui.connected_dict[conn_id] = executor
    else:
        executor = gui.connected_dict.get(conn_id)
    return executor


def close_connection(gui, conn_id):
    """关闭连接，清空选中内容"""
    if conn_id and gui.connected_dict.get(conn_id):
        gui.connected_dict.get(conn_id).exit()
        del gui.connected_dict[conn_id]
    else:
        [executor.exit() for executor in gui.connected_dict.values()]
        gui.connected_dict.clear()


def add_conn_func(gui):
    """添加连接，打开弹窗，接收输入，保存系统库"""
    conn_info = Connection(None, None, None, None, None, None)
    show_conn_dialog(gui, conn_info, ADD_CONN_MENU)


def show_conn_dialog(gui, conn_info, title):
    """打开添加、编辑连接子窗口"""
    dialog = Ui_Dialog(conn_info, title, gui)
    dialog.setWindowModality(Qt.ApplicationModal)
    dialog.show()
    if title == ADD_CONN_MENU:
        dialog.conn_signal.connect(add_conn_tree_item)
    elif title == EDIT_CONN_MENU:
        dialog.conn_signal.connect(update_conn_tree_item)


def add_conn_tree_item(gui, connection):
    """添加树节点（连接）"""
    gui.conns_dict[connection.id] = connection
    make_tree_item(gui.treeWidget, connection.name, connection.id)


def update_conn_tree_item(gui, connection):
    """更新树节点"""
    gui.conns_dict[connection.id] = connection
    item = gui.treeWidget.currentItem()
    gui.update_tree_item_name(item, connection.name)


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
            # 将checkbox选中状态放入集合，状态只有选中与未选中，
            # 若集合元素为两个，则为部分选中，若为一个，取值判断。
            check_set.add(parent.child(index).checkState(0))
        if len(check_set) == 2:
            parted_checked = True
        elif check_set.pop() == Qt.Checked:
            all_checked = True
    return all_checked, parted_checked


def check_field_status(gui, item):
    """
    检查字段是否全选
    :return all_checked: 是否被全选
            parted_checked: 是否部分选中
    """
    parted_checked = False
    # 根据表头复选框状态判断是否全选
    all_checked = gui.header.isOn
    # 如果表头没有全选，左侧表选中，证明是部分选中
    if not all_checked and item.checkState(0) == Qt.Checked:
        parted_checked = True
    return all_checked, parted_checked


def close_tree_item(gui, item):
    """关闭树的某项，将其下所有子项移除，并将扩展状态置为false"""
    # 移除所有子项目
    item.takeChildren()
    close_table(gui)


def make_tree_item(gui, parent, name, item_id=None, checkbox=None):
    """构造树的子项"""
    item = QTreeWidgetItem(parent)
    gui.update_tree_item_name(item, name)
    if item_id:
        # id 作为隐藏属性，写于第二列
        gui.update_tree_item_name(item, str(item_id), 1)
    if checkbox is not None:
        item.setCheckState(0, checkbox)


def quit_app(gui):
    gui.main_window.close()


def set_children_check_state(item, check_state):
    for index in range(item.childCount()):
        item.child(index).setCheckState(0, check_state)
