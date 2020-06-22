﻿# -*- coding: utf-8 -*-
from constant import *
_author_ = 'luwt'
_date_ = '2020/6/22 15:41'


def get_conn_menu_names(item):
    """生成第一层，连接列表的右键菜单名称"""
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
    @:param item 当前点击的库，如果库下面有子元素，那么就只需要关闭数据库菜单
    @:param checked 元祖：其中包含两个布尔值，第一个代表是否全选，第二个代表是否部分选中
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


def get_table_menu_names():
    """
    生成第三层，数据表列表的右键菜单

    """
    menu_names = list()
    menu_names.append(OPEN_TABLE_MENU)
    menu_names.append(CLOSE_TABLE_MENU)
    menu_names.append(SELECT_ALL_FIELD_MENU)
    menu_names.append(UNSELECT_FIELD_MENU)
    menu_names.append(GENERATE_MENU)
    return menu_names


