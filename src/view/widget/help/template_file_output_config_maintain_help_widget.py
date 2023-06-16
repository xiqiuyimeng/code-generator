# -*- coding: utf-8 -*-
from src.constant.help.template_file_output_config_maintain_help_constant import *
from src.view.widget.help.help_widget_abc import HelpWidgetABC

_author_ = 'luwt'
_date_ = '2023/6/15 11:59'


class TemplateFileOutputConfigMaintainHelpWidget(HelpWidgetABC):

    def add_content(self):
        self.add_label(OVERVIEW_TEXT)
        self.add_row_label(OPERATE_LABEL_TEXT, OPERATE_HELP_TEXT)
