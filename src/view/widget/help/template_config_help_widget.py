# -*- coding: utf-8 -*-
from src.constant.help.template_config_help_constant import *
from src.view.widget.help.help_widget_abc import HelpWidgetABC

_author_ = 'luwt'
_date_ = '2023/6/15 11:59'


class TemplateConfigHelpWidget(HelpWidgetABC):

    def add_content(self):
        self.add_label(OVERVIEW_TEXT)
        self.add_row_text_browser(TEMPLATE_CONFIG_INFO_LABEL_TEXT, TEMPLATE_CONFIG_INFO_HELP_TEXT)
        self.add_row_text_browser(TEMPLATE_CONFIG_WIDGET_LABEL_TEXT, TEMPLATE_CONFIG_WIDGET_HELP_TEXT)
