# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLabel

from src.constant.table_constant import TABLE_HEADER_FIRST_COL_LABEL
from src.view.table.table_header.abstract_table_header import AbstractTableHeader
from src.view.table.table_item.table_item import make_checkbox_num_widget_with_button

_author_ = 'luwt'
_date_ = '2023/2/28 17:27'


class CheckBoxHeader(AbstractTableHeader):
    """普通复选框表头"""

    def __init__(self, header_labels, parent_table):
        self.header_labels = header_labels
        # 表头1行
        super().__init__(1, len(header_labels) + 1, parent_table, parent_table)

    def setup_header_items(self):
        [self.setItem(0, col, self.make_item(header_text))
         for col, header_text in enumerate(self.header_labels, start=1)]


class CheckBoxHeaderWithButton(CheckBoxHeader):

    def get_checkbox_num_widget(self):
        return make_checkbox_num_widget_with_button(TABLE_HEADER_FIRST_COL_LABEL,
                                                    self.click_header_checkbox, QLabel())
