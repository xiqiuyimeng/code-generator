# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt

from src.view.table.table_header.check_box_table_header import CheckBoxHeader
from src.view.table.table_item.table_item import make_checkbox_num_widget
from src.view.table.table_widget.ds_table_widget.ds_col_table_widget_abc import DsColTableWidgetABC
from src.view.tree.tree_item.tree_item_func import get_add_del_data

_author_ = 'luwt'
_date_ = '2022/5/10 15:25'


class SqlDsColTableWidget(DsColTableWidgetABC):

    def get_header(self, header_labels):
        return CheckBoxHeader(header_labels, self)

    def make_checkbox_num_widget(self, row_index, col_data):
        return make_checkbox_num_widget(row_index + 1, self.click_row_checkbox)

    def fill_post_process(self):
        checked_list = list()
        # 循环设置选中项
        for row, col in enumerate(self.cols):
            if col.checked:
                checked_list.append(col)
                self.cellWidget(row, 0).check_box.setCheckState(Qt.CheckState.Checked)
        # 将选中项保存到选中树结构中
        if checked_list:
            self.add_checked_data(checked_list)

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
