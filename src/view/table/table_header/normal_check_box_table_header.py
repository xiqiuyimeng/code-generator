# -*- coding: utf-8 -*-
from src.view.table.table_header.abstract_table_header import AbstractTableHeader

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
