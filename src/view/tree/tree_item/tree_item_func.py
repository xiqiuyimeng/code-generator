# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt

_author_ = 'luwt'
_date_ = '2022/10/1 17:55'


def set_item_opened_record(item, opened_item_record):
    # 放入历史记录表中的记录
    item.setData(0, Qt.UserRole, opened_item_record)


def get_item_opened_record(item):
    return item.data(0, Qt.UserRole)


def set_item_opened_tab(item, tab_widget):
    # 放入打开的tab_widget
    item.setData(1, Qt.UserRole, tab_widget)


def get_item_opened_tab(item):
    return item.data(1, Qt.UserRole)


def link_table_checkbox(tree_item, check_state):
    # 联动表格复选框
    tab = get_item_opened_tab(tree_item)
    if tab:
        table_widget = tab.table_frame.table_widget
        table_widget.table_header.change_header_state(check_state)
        # 批量处理数据保存
        table_widget.batch_deal_checked(check_state)


def get_children_opened_ids(parent_item):
    return list(map(lambda x: x.id, recursive_get_children_opened_items(parent_item)))


def recursive_get_children_opened_items(parent_item):
    child_count = parent_item.childCount()
    if child_count:
        for index in range(child_count):
            child_item = parent_item.child(index)
            yield get_item_opened_record(child_item)
            yield from recursive_get_children_opened_items(child_item)


def get_children_items(parent_item):
    children_items = list()
    for idx in range(parent_item.childCount()):
        children_items.append(parent_item.child(idx))
    return children_items


def get_add_del_data(item):
    add_del_data = dict()
    recursive_get_add_del_data(item, add_del_data)
    return add_del_data


def recursive_get_add_del_data(item, data_dict):
    if item.parent():
        recursive_get_add_del_data(item.parent(), data_dict)
    opened_record = get_item_opened_record(item)
    data_dict[opened_record.level] = opened_record


def save_tree_data(item, tree_data):
    # 如果表已打开，选中数据处理委托给表复选框处理，
    # 表格未打开，那么执行树节点选中数据处理
    tab = get_item_opened_tab(item)
    if not tab:
        check_state = item.checkState(0)
        add_del_data = get_add_del_data(item)
        if check_state == Qt.Checked:
            # 如果是选中，添加选中数据
            tree_data.add_node(add_del_data)
        elif check_state == Qt.Unchecked:
            # 如果是未选中，删除选中数据
            tree_data.del_node(add_del_data)
