# -*- coding: utf-8 -*-
from src.constant.help.ds_col_type_help_constant import *
from src.view.widget.help.help_widget_abc import HelpWidgetABC

_author_ = 'luwt'
_date_ = '2023/6/15 11:58'


class DsColTypeHelpWidget(HelpWidgetABC):

    def add_content(self):
        self.add_label(OVERVIEW_TEXT)
