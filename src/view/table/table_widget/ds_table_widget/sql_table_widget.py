# -*- coding: utf-8 -*-

from src.view.table.table_widget.ds_table_widget.abstract_ds_col_table_widget import AbstractDsColTableWidget
from src.view.tree.tree_item.tree_item_func import get_add_del_data

_author_ = 'luwt'
_date_ = '2022/5/10 15:25'


class SqlDsColTableWidget(AbstractDsColTableWidget):

    def add_checked_data(self, cols):
        add_data = get_add_del_data(self.tree_item)
        add_data[max(add_data) + 1] = cols
        self.tree_data.add_node(add_data)

    def remove_checked_data(self, col):
        del_data = get_add_del_data(self.tree_item)
        del_data[max(del_data) + 1] = col
        self.tree_data.del_node(del_data)

    def remove_all_table_checked(self, cols):
        # 对于sql数据源表来说，不需要使用列，移除所有选中列，等于取消选中表，所以直接操作表即可
        del_data = get_add_del_data(self.tree_item)
        self.tree_data.del_node(del_data)

    def update_checked_data(self, col_data):
        update_data = get_add_del_data(self.tree_item)
        update_data[max(update_data) + 1] = col_data
        self.tree_data.update_node_name(update_data)
