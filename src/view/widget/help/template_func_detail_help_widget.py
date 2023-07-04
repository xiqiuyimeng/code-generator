# -*- coding: utf-8 -*-
from src.constant.help.template_func_detail_help_constant import *
from src.view.widget.help.help_widget_abc import HelpWidgetABC

_author_ = 'luwt'
_date_ = '2023/6/15 12:00'


class TemplateFuncDetailHelpWidget(HelpWidgetABC):

    def add_content(self):
        self.add_label(OVERVIEW_TEXT)
        self.add_row_label(TEMPLATE_FUNC_NAME_LABEL_TEXT, TEMPLATE_FUNC_NAME_HELP_TEXT)
        self.add_row_label(TEMPLATE_FUNC_EDIT_LABEL_TEXT, TEMPLATE_FUNC_EDIT_HELP_TEXT)
