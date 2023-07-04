# -*- coding: utf-8 -*-
from src.constant.help.type_mapping_table_help_constant import *
from src.view.widget.help.help_widget_abc import HelpWidgetABC

_author_ = 'luwt'
_date_ = '2023/6/15 11:58'


class TypeMappingTableHelpWidget(HelpWidgetABC):

    def add_content(self):
        self.add_label(OVERVIEW_TEXT)
        self.add_row_label(TYPE_MAPPING_TABLE_LABEL_TEXT, TYPE_MAPPING_TABLE_HELP_TEXT)
        self.add_row_label(DS_COL_TYPE_LABEL_TEXT, DS_COL_TYPE_HELP_TEXT)
