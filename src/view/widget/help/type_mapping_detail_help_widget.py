# -*- coding: utf-8 -*-
from src.constant.help.type_mapping_detail_help_constant import *
from src.view.widget.help.help_widget_abc import HelpWidgetABC

_author_ = 'luwt'
_date_ = '2023/6/15 11:58'


class TypeMappingDetailHelpWidget(HelpWidgetABC):

    def add_content(self):
        self.add_label(OVERVIEW_TEXT)
        self.add_row_label(BASIC_INFO_LABEL_TEXT, BASIC_INFO_HELP_TEXT)
        self.add_row_text_browser(COL_TYPE_MAPPING_LABEL_TEXT, COL_TYPE_MAPPING_HELP_TEXT)
