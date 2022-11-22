# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt

_author_ = 'luwt'
_date_ = '2022/10/1 17:55'


def set_item_opened_record(item, opened_item_record):
    # 放入历史记录表中的记录
    item.setData(0, Qt.UserRole, opened_item_record)


def get_item_opened_record(item):
    return item.data(0, Qt.UserRole)


def set_item_no_change(item, changed):
    # 放入节点是否无变化的标志位，以便禁止一些场景下的节点改变信号事件
    item.setData(1, Qt.UserRole, changed)


def get_item_no_change(item):
    # 无变化的标志位，只使用一次就可以了，所以应该在获取的时候，即重置
    data = item.data(1, Qt.UserRole)
    set_item_no_change(item, None)
    return data


def set_item_opened_tab(item, tab_widget):
    # 放入打开的tab_widget
    item.setData(2, Qt.UserRole, tab_widget)


def get_item_opened_tab(item):
    return item.data(2, Qt.UserRole)


def get_item_sql_conn(item):
    return item.data(3, Qt.UserRole)


def set_item_sql_conn(item, sql_conn):
    # 放入连接信息
    item.setData(3, Qt.UserRole, sql_conn)


def get_item_conn_type(item):
    return item.data(4, Qt.UserRole)


def set_item_conn_type(item, conn_type):
    # 放入连接类型
    item.setData(4, Qt.UserRole, conn_type)


def link_table_checkbox(tree_item, check_state):
    # 联动表格复选框
    tab = get_item_opened_tab(tree_item)
    if tab:
        table_widget = tab.table_frame.table_widget
        table_widget.table_header.change_header_state(check_state)
        # 批量处理数据保存
        table_widget.batch_update_check_state(check_state)


def get_children_opened_ids(parent_item):
    return list(map(lambda x: x.id, recursive_get_children_opened_items(parent_item)))


def recursive_get_children_opened_items(parent_item):
    child_count = parent_item.childCount()
    if child_count:
        for index in range(child_count):
            child_item = parent_item.child(index)
            yield get_item_opened_record(child_item)
            yield from recursive_get_children_opened_items(child_item)
