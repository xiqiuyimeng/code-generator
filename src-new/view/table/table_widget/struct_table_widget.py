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

    def do_add_child_table(self, children_cols, row_index) -> QWidget:
        child_widget = QWidget()
        # 维护树节点引用，方便子表格使用
        child_widget.tree_item = self.tree_item
        child_layout = QHBoxLayout()
        child_widget.setLayout(child_layout)
        # 创建子表格
        child_table = StructTableWidget(self.main_window, child_widget, children_cols)
        child_widget.child_table = child_table
        child_layout.addWidget(child_table)

        child_table.fill_table()

        child_table.parent_table = self
        return child_widget

    def add_checked_data(self, cols): ...

    def remove_checked_data(self, cols): ...

    def remove_all_table_checked(self): ...

    def save_data(self, row, col, data):
        # 根据row找到对应的列信息数据
        col_data = self.cols[row]
        modify_col_data = DsTableColInfo()
        modify_col_data.id = col_data.id

        if col == 0:
            col_data.checked = data
            modify_col_data.checked = data
        elif col == 1:
            col_data.col_name = data
            modify_col_data.col_name = data
        elif col == 2:
            col_data.data_type = data
            modify_col_data.data_type = data
        elif col == 3:
            col_data.full_data_type = data
            modify_col_data.full_data_type = data
        elif col == 4:
            is_pk = 1 if data == '是' else 0
            col_data.is_pk = is_pk
            modify_col_data.is_pk = is_pk
        elif col == 5:
            col_data.col_comment = data
            modify_col_data.col_comment = data

        # 保存到树选中数据中，由于保存的列对象是从 self.cols中取的，
        # 所以树中保存的列对象引用指向列表中对象，在数据变化时，无需手动同步
        # 如果是选中，则为添加数据，否则为删除数据
        if col_data.checked:
            self.add_checked_data(col_data)
        else:
            self.remove_checked_data(col_data)

        # 保存数据
        self.async_save_executor.save_table_data(modify_col_data)
