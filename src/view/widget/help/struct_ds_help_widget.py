# -*- coding: utf-8 -*-
from src.constant.help.struct_ds_help_constant import *
from src.view.widget.help.help_widget_abc import HelpWidgetABC

_author_ = 'luwt'
_date_ = '2023/6/15 11:57'


class StructDsHelpWidget(HelpWidgetABC):

    def add_content(self):
        self.add_label(OVERVIEW_TEXT)
        self.add_row_text_browser(STRUCT_CLASSIFY_LABEL_TEXT, STRUCT_CLASSIFY_HELP_TEXT)
        self.add_row_text_browser(JSON_LABEL_TEXT, JSON_HELP_TEXT)
