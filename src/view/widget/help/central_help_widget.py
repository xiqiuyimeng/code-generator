# -*- coding: utf-8 -*-
from src.constant.help.central_help_constant import *
from src.view.widget.help.help_widget_abc import HelpWidgetABC

_author_ = 'luwt'
_date_ = '2023/6/14 15:54'


class CentralHelpWidget(HelpWidgetABC):

    def add_content(self):
        self.add_label(OVERVIEW_TEXT)
        self.add_row_label(TITLE_BAR_LABEL_TEXT, TITLE_BAR_HELP_TEXT)
        self.add_row_text_browser(MENU_BAR_LABEL_TEXT, MENU_BAR_HELP_TEXT)
        self.add_row_text_browser(TOOL_BAR_LABEL_TEXT, TOOL_BAR_HELP_TEXT)
        self.add_row_text_browser(MAIN_AREA_LABEL_TEXT, MAIN_AREA_HELP_TEXT)

