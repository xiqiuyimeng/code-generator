# -*- coding: utf-8 -*-
from src.constant.help.template_copy_func_help_constant import *
from src.view.widget.help import HelpWidgetABC

_author_ = 'luwt'
_date_ = '2023/6/26 14:51'


class TemplateCopyFuncHelpWidget(HelpWidgetABC):

    def add_content(self):
        self.add_label(OVERVIEW_TEXT)
        self.add_row_label(TEMPLATE_LIST_LABEL_TEXT, TEMPLATE_LIST_HELP_TEXT)
        self.add_row_text_browser(TEMPLATE_FUNC_LABEL_TEXT, TEMPLATE_FUNC_HELP_TEXT)
