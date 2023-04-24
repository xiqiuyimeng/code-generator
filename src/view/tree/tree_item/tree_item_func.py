# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt

from src.constant.icon_enum import get_icon

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
        table_widget.table_header.link_header_check_state(check_state)
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


def refresh_tree_item_callback(tree_widget, item, item_changed_dict, handle_unchanged_func,
                               handle_delete_func, make_new_item_func, refresh_executor=None):
    """刷新树节点，页面处理方法"""
    # 清空选中数据
    del_data = get_add_del_data(item)
    tree_widget.tree_data.del_node(del_data)

    new_item_records = item_changed_dict.get('new')
    exists_item_records = item_changed_dict.get('exists')
    delete_item_records = item_changed_dict.get('delete')
    unchanged_item_records = item_changed_dict.get('unchanged')
    sort_order = item_changed_dict.get('sort')

    # 1. 首先处理没有变化的元素
    for unchanged_item_record in unchanged_item_records:
        unchanged_item = item.child(unchanged_item_record.item_order - 1)
        if refresh_executor:
            handle_unchanged_func(unchanged_item, refresh_executor)
        else:
            handle_unchanged_func(unchanged_item)
    # 2. 处理需要更新的元素
    for old_item_order, exists_item_record in exists_item_records:
        update_item = item.child(old_item_order - 1)
        set_item_opened_record(update_item, exists_item_record)
        if refresh_executor:
            handle_unchanged_func(update_item, refresh_executor)
        else:
            handle_unchanged_func(update_item)
    # 3. 处理删除的元素
    for delete_item_record in delete_item_records:
        del_item = item.child(delete_item_record.item_order - 1)
        if refresh_executor:
            handle_delete_func(del_item, refresh_executor)
        else:
            handle_delete_func(del_item)
        # 删除树节点
        item.removeChild(del_item)
    # 4. 最后处理需要插入的节点元素
    if new_item_records:
        icon = get_icon(get_item_opened_record(item).data_type.tb_icon_name)
        for new_item_record in new_item_records:
            # 直接添加节点，最后统一排序
            make_new_item_func(tree_widget, item, new_item_record.item_name,
                               icon, new_item_record, Qt.Unchecked)
    if sort_order:
        item.sortChildren(0, Qt.SortOrder.AscendingOrder)


def set_item_output_config(item, output_config):
    # 放入输出配置
    item.setData(0, Qt.UserRole, output_config)


def get_item_output_config(item):
    return item.data(0, Qt.UserRole)


def set_item_template_file(item, template_file):
    # 放入模板文件
    item.setData(0, Qt.UserRole, template_file)


def get_item_template_file(item):
    return item.data(0, Qt.UserRole)
