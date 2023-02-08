# -*- coding: utf-8 -*-
"""
表格结构，大体与树结构类似
"""
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from src.view.table.table_widget.abstract_table_widget import AbstractTableWidget
from src.view.tree.tree_item.tree_item_func import get_add_del_data

_author_ = 'luwt'
_date_ = '2022/5/10 15:25'


class StructTableWidget(AbstractTableWidget):

    def do_add_child_table(self, col_data, row_index) -> QWidget:
        child_widget = QWidget()
        # 维护树节点引用，方便子表格使用
        child_widget.tree_item = self.tree_item
        child_layout = QHBoxLayout()
        child_widget.setLayout(child_layout)
        # 创建子表格
        child_table = StructTableWidget(self.main_window, self.tree_widget, child_widget,
                                        col_data.children, self)
        child_widget.child_table = child_table
        child_layout.addWidget(child_table)

        # 连接表头信号，当子表表头变化时，应该触发父表对应行复选框变化
        child_table.table_header.header_check_state_changed.connect(
            lambda check_state: self.change_parent_col_check_state(check_state, col_data))

        child_table.fill_table()
        return child_widget

    def change_parent_col_check_state(self, check_state, col_data):
        # 获取子表在父表中的实际行索引，当前行之前的行（列数据列表）
        row_index = self.cols.index(col_data)
        # 设置列复选框状态，设置状态后，将触发checkbox的信号：not_click_state_changed，从而触发父表表头变化
        self.table_header.checkbox_list[row_index].setCheckState(check_state)

    def get_add_del_col_data(self, add_del_data, checked_cols):
        """根据选中数据获取表层次的数据，由于选择的列数据是最底层，所以需要依次推导出上一层节点，构造层次数据"""
        # 获取父列数据，选中的列一定属于同一个表格内，所以它们拥有共同的父列
        parent_col = checked_cols[0].parent_col if isinstance(checked_cols, list) else checked_cols.parent_col
        # 如果父列存在，那么继续寻找上一层
        if parent_col:
            self.get_add_del_col_data(add_del_data, parent_col)
        # 构建表层次数据
        add_del_data[max(add_del_data) + 1] = checked_cols

    def add_checked_data(self, cols):
        # 首先获取树节点层次数据
        add_data = get_add_del_data(self.tree_item)
        # 获取表层次数据
        self.get_add_del_col_data(add_data, cols)
        self.tree_data.add_node(add_data)

    def remove_checked_data(self, cols):
        # 首先获取树节点层次数据
        del_data = get_add_del_data(self.tree_item)
        # 获取表层次数据
        self.get_add_del_col_data(del_data, cols)
        self.tree_data.del_node(del_data)

    def remove_all_table_checked(self, cols):
        self.remove_checked_data(cols)

    def update_checked_data(self, col_data):
        # 首先获取树节点层次数据
        update_data = get_add_del_data(self.tree_item)
        # 获取表层次数据
        self.get_add_del_col_data(update_data, col_data)
        self.tree_data.update_node_name(update_data)

