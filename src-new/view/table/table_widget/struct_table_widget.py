# -*- coding: utf-8 -*-
"""
表格结构，大体与树结构类似
"""
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from service.async_func.async_tab_table_task import AsyncSaveTabObjExecutor
from service.system_storage.ds_table_col_info_sqlite import DsTableColInfo
from service.util.tree_node import TreeData
from view.table.table_widget.abstract_table_widget import AbstractTableWidget

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

        child_table.fill_table()
        return child_widget

    def add_checked_data(self, cols):
        pass

    def remove_checked_data(self, cols): ...

    def remove_all_table_checked(self): ...

