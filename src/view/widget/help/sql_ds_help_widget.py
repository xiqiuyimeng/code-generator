# -*- coding: utf-8 -*-
from src.constant.help.sql_ds_help_constant import *
from src.view.widget.help.help_widget_abc import HelpWidgetABC

_author_ = 'luwt'
_date_ = '2023/6/15 11:57'


class SqlDsHelpWidget(HelpWidgetABC):

    def add_content(self):
        self.add_label(OVERVIEW_TEXT)
        self.add_row_label(SQLITE_LABEL_TEXT, SQLITE_HELP_TEXT)
        self.add_row_text_browser(MYSQL_LABEL_TEXT, MYSQL_HELP_TEXT)
        self.add_row_text_browser(ORACLE_LABEL_TEXT, ORACLE_HELP_TEXT)
