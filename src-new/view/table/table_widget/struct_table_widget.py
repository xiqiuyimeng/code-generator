# -*- coding: utf-8 -*-
"""
表格结构，大体与树结构类似
"""
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from service.async_func.async_tab_table_task import AsyncSaveTabObjExecutor
from service.system_storage.ds_table_col_info_sqlite import DsTableColInfo
from service.util.tree_node import TreeData
from view.table.table_widget.abstract_table_widget import AbstractTableWidget
from view.tree.tree_item.tree_item_func import get_add_del_data

_author_ = 'luwt'
_date_ = '2022/5/10 15:25'


class StructTableWidget(AbstractTableWidget):

    def get_async_save_executor(self) -> AsyncSaveTabObjExecutor:
        return self.main_window.struct_tab_widget.async_save_executor

    def get_tree_data(self) -> TreeData:
        return self.main_window.struct_tree_widget.tree_data

    def do_add_child_table(self, col_data, row_index) -> QWidget:
        child_widget = QWidget()
        # 维护树节点引用，方便子表格使用
        child_widget.tree_item = self.tree_item
        child_layout = QHBoxLayout()
        child_widget.setLayout(child_layout)
        # 创建子表格
        child_table = StructTableWidget(self.main_window, child_widget, col_data.children, self, col_data)
        child_widget.child_table = child_table
        child_layout.addWidget(child_table)

        # 连接表头信号，当子表表头变化时，应该触发父表对应行复选框变化
        child_table.table_header.header_check_state.connect(
            lambda check_state: self.change_parent_col_check_state(check_state, col_data))

        child_table.fill_table()
        return child_widget

    def change_parent_col_check_state(self, check_state, col_data):
        # 获取子表在父表中的实际行索引，当前行之前的行（列数据列表）
        row_index = self.cols.index(col_data)
        # 设置列复选框状态
        self.table_header.checkbox_list[row_index].setCheckState(check_state)

    def get_add_del_col_data(self, add_del_data, table: AbstractTableWidget, checked_cols):
        if table.parent_col and table.parent_col.checked:
            self.get_add_del_col_data(add_del_data, table.parent_table, table.parent_col)
        add_del_data[max(add_del_data) + 1] = checked_cols

    def add_checked_data(self, cols):
        # 首先获取树节点层次数据
        add_data = get_add_del_data(self.tree_item)
        # 获取表层次数据
        self.get_add_del_col_data(add_data, self, cols)
        self.tree_data.add_node(add_data)

    def remove_checked_data(self, cols):
        # 首先获取树节点层次数据
        del_data = get_add_del_data(self.tree_item)
        # 获取表层次数据
        self.get_add_del_col_data(del_data, self, cols)
        self.tree_data.del_node(del_data)

    def remove_all_table_checked(self): ...

