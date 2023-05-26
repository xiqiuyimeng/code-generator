# -*- coding: utf-8 -*-

from src.constant.table_constant import TYPE_MAPPING_TABLE_HEADER_LABELS
from src.view.table.table_widget.custom_export_table_widget import CustomCopyExportTableWidget

_author_ = 'luwt'
_date_ = '2023/2/13 11:09'


class TypeMappingTableWidget(CustomCopyExportTableWidget):

    def __init__(self, *args):
        super().__init__(TYPE_MAPPING_TABLE_HEADER_LABELS, *args)

    def do_fill_row(self, row_index, type_mapping, fill_create_time=True):
        self.setItem(row_index, 1, self.make_item(type_mapping.mapping_name))
        self.setItem(row_index, 2, self.make_item(type_mapping.ds_type))
        self.setItem(row_index, 3, self.make_item(type_mapping.comment))
        if fill_create_time:
            self.setItem(row_index, 4, self.make_item(type_mapping.create_time))
        self.setItem(row_index, 5, self.make_item(type_mapping.update_time))

    def del_duplicate_rows(self, duplicate_data_list):
        # 根据名称删除
        duplicate_names = tuple(data.mapping_name for data in duplicate_data_list)
        for row in reversed(range(self.rowCount())):
            if self.item(row, 1).text() in duplicate_names:
                self.del_row(row)
