# -*- coding: utf-8 -*-
from src.constant.table_constant import TEMPLATE_TABLE_HEADER_LABELS
from src.view.table.table_widget.custom_export_table_widget import CustomCopyExportTableWidget

_author_ = 'luwt'
_date_ = '2023/3/8 17:59'


class TemplateTableWidget(CustomCopyExportTableWidget):

    def __init__(self, *args):
        super().__init__(TEMPLATE_TABLE_HEADER_LABELS, *args)

    def do_fill_row(self, row_index, template, fill_create_time=True):
        self.setItem(row_index, 1, self.make_item(template.template_name))
        self.setItem(row_index, 2, self.make_item(template.template_desc))
        if fill_create_time:
            self.setItem(row_index, 3, self.make_item(template.create_time))
        self.setItem(row_index, 4, self.make_item(template.update_time))

    def get_duplicate_name(self, data):
        return data.template_name
