# -*- coding: utf-8 -*-
"""
处理右键菜单
"""
from PyQt5.QtCore import Qt

from src.constant.constant import CLOSE_CONN_MENU, OPEN_CONN_MENU, TEST_CONN_MENU, \
    ADD_CONN_MENU, EDIT_CONN_MENU, DEL_CONN_MENU, CLOSE_DB_MENU, UNSELECT_TB_MENU, \
    SELECT_ALL_TB_MENU, OPEN_DB_MENU, CLOSE_TABLE_MENU, UNSELECT_FIELD_MENU, \
    SELECT_ALL_FIELD_MENU, OPEN_TABLE_MENU

_author_ = 'luwt'
_date_ = '2020/6/22 15:41'


def get_conn_menu_names(item):
    """
    生成第一层，连接列表的右键菜单名称
    :param item 当前点击的连接
    """
    menu_names = list()
    if item.childCount():
        menu_names.append(CLOSE_CONN_MENU)
    else:
        menu_names.append(OPEN_CONN_MENU)
        menu_names.append(TEST_CONN_MENU)
    menu_names.append(ADD_CONN_MENU)
    menu_names.append(EDIT_CONN_MENU)
    menu_names.append(DEL_CONN_MENU)
    return menu_names


def get_db_menu_names(item, checked):
    """
    生成第二层，数据库列表的右键菜单名称
    :param item 当前点击的库，如果库下面有子元素，那么就只需要关闭数据库菜单
    :param checked 元祖：其中包含两个布尔值，
        第一个代表是否全选，第二个代表是否部分选中
    菜单：
        全选：添加取消选择菜单
        部分选中：添加全选菜单和取消选择菜单
        都未选中：添加全选菜单
    """
    menu_names = list()
    if item.childCount():
        menu_names.append(CLOSE_DB_MENU)
        # 全选时：添加取消选择菜单
        if checked[0]:
            menu_names.append(UNSELECT_TB_MENU)
        # 部分选中时：添加全选菜单和取消选择菜单
        elif checked[1]:
            menu_names.append(SELECT_ALL_TB_MENU)
            menu_names.append(UNSELECT_TB_MENU)
        # 都未选中时：添加全选菜单
        else:
            menu_names.append(SELECT_ALL_TB_MENU)
    else:
        menu_names.append(OPEN_DB_MENU)
    return menu_names


def get_table_menu_names(table_opened, check_state):
    """
    生成第三层，数据表列表的右键菜单
    :param table_opened 表是否打开
    :param check_state: 字符串，checkbox的选中状态：
        全选：添加取消选择菜单
        部分选中：添加全选菜单和取消选择菜单
        都未选中：添加全选菜单
    """
    menu_names = list()
    if table_opened:
        menu_names.append(CLOSE_TABLE_MENU)
        # 全选时：添加取消选择菜单
        if int(check_state) == Qt.Checked:
            menu_names.append(UNSELECT_FIELD_MENU)
        # 部分选中时：添加全选菜单和取消选择菜单
        elif int(check_state) == Qt.PartiallyChecked:
            menu_names.append(SELECT_ALL_FIELD_MENU)
            menu_names.append(UNSELECT_FIELD_MENU)
        # 都未选中时：添加全选菜单
        elif int(check_state) == Qt.Unchecked:
            menu_names.append(SELECT_ALL_FIELD_MENU)
    else:
        menu_names.append(OPEN_TABLE_MENU)
    return menu_names

