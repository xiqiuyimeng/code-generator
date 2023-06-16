# -*- coding: utf-8 -*-
from src.constant.help.import_error_data_help_constant import *
from src.view.widget.help.help_widget_abc import HelpWidgetABC

_author_ = 'luwt'
_date_ = '2023/6/15 12:00'


class ImportErrorDataHelpWidget(HelpWidgetABC):

    def add_content(self):
        self.add_label(OVERVIEW_TEXT)
        self.add_row_label(DUPLICATE_DATA_LABEL_TEXT, DUPLICATE_DATA_HELP_TEXT)
        self.add_row_label(ERROR_DATA_LABEL_TEXT, ERROR_DATA_HELP_TEXT)
