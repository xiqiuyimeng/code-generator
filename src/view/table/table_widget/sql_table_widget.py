# -*- coding: utf-8 -*-

from service.async_func.async_tab_table_task import AsyncSaveTabObjExecutor
from service.util.tree_node import TreeData
from view.table.table_widget.abstract_table_widget import AbstractTableWidget
from view.tree.tree_item.tree_item_func import get_add_del_data

_author_ = 'luwt'
_date_ = '2022/5/10 15:25'


class SqlTableWidget(AbstractTableWidget):

    def get_async_save_executor(self) -> AsyncSaveTabObjExecutor:
        return self.main_window.sql_tab_widget.async_save_executor

    def get_tree_data(self) -> TreeData:
        return self.main_window.sql_tree_widget.tree_data

    def add_checked_data(self, cols):
        add_data = get_add_del_data(self.tree_item)
        add_data[max(add_data) + 1] = cols
        self.tree_data.add_node(add_data)

    def remove_checked_data(self, col):
        del_data = get_add_del_data(self.tree_item)
        del_data[max(del_data) + 1] = col
        self.tree_data.del_node(del_data)

    def remove_all_table_checked(self):
        del_data = get_add_del_data(self.tree_item)
        self.tree_data.del_node(del_data)
