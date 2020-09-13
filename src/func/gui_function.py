# -*- coding: utf-8 -*-
"""
处理主窗口对象相关功能
"""
from PyQt5.QtCore import Qt

_author_ = 'luwt'
_date_ = '2020/7/2 15:57'


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
    将当前节点下所有项的复选框统一改为一个状态
    :param item: 当前点击的树节点元素
    :param check_state: 复选框状态
    """
    for index in range(item.childCount()):
        item.child(index).setCheckState(0, check_state)

