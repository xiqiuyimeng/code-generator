# -*- coding: utf-8 -*-
from src.constant.help.import_data_help_constant import *
from src.view.widget.help.help_widget_abc import HelpWidgetABC

_author_ = 'luwt'
_date_ = '2023/6/15 12:00'


class ImportDataHelpWidget(HelpWidgetABC):

    def add_content(self):
        self.add_label(OVERVIEW_TEXT)
        self.add_row_text_browser(IMPORT_DATA_TYPE_LABEL_TEXT, IMPORT_DATA_TYPE_HELP_TEXT)
        self.add_row_label(IMPORT_FILE_TYPE_LABEL_TEXT, IMPORT_FILE_TYPE_HELP_TEXT)
        self.add_row_label(IMPORT_ERROR_HANDLE_LABEL_TEXT, IMPORT_ERROR_HANDLE_HELP_TEXT)
