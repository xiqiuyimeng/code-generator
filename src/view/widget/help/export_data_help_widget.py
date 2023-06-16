# -*- coding: utf-8 -*-
from src.constant.help.export_data_help_constant import *
from src.view.widget.help.help_widget_abc import HelpWidgetABC

_author_ = 'luwt'
_date_ = '2023/6/15 12:00'


class ExportDataHelpWidget(HelpWidgetABC):

    def add_content(self):
        self.add_label(OVERVIEW_TEXT)
        self.add_row_text_browser(EXPORT_DATA_TYPE_LABEL_TEXT, EXPORT_DATA_TYPE_HELP_TEXT)
        self.add_row_label(EXPORT_FILE_LABEL_TEXT, EXPORT_FILE_HELP_TEXT)
