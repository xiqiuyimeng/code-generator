# -*- coding: utf-8 -*-

from src.constant.table_constant import TYPE_MAPPING_TABLE_HEADER_LABELS
from src.view.table.table_widget.custom_table_widget import CustomTableWidget

_author_ = 'luwt'
_date_ = '2023/2/13 11:09'


class TypeMappingTableWidget(CustomTableWidget):

    def __init__(self, *args):
        super().__init__(TYPE_MAPPING_TABLE_HEADER_LABELS, *args)

    def _do_fill_row(self, row_index, type_mapping, fill_create_time=True):
        self.setItem(row_index, 1, self.make_item(type_mapping.mapping_name))
        self.setItem(row_index, 2, self.make_item(type_mapping.ds_type))
        self.setItem(row_index, 3, self.make_item(type_mapping.comment))
        if fill_create_time:
            self.setItem(row_index, 4, self.make_item(type_mapping.create_time))
        self.setItem(row_index, 5, self.make_item(type_mapping.update_time))
