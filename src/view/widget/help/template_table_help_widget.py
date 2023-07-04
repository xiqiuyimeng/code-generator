# -*- coding: utf-8 -*-
from src.constant.help.template_table_help_constant import *
from src.view.widget.help.help_widget_abc import HelpWidgetABC

_author_ = 'luwt'
_date_ = '2023/6/15 11:58'


class TemplateTableHelpWidget(HelpWidgetABC):

    def add_content(self):
        self.add_label(OVERVIEW_TEXT)
        self.add_row_label(TEMPLATE_TABLE_LABEL_TEXT, TEMPLATE_TABLE_HELP_TEXT)
        self.add_row_label(TEMPLATE_FUNC_LABEL_TEXT, TEMPLATE_FUNC_HELP_TEXT)
