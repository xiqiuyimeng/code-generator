# -*- coding: utf-8 -*-
from src.constant.template_dialog_constant import CHECK_VAR_CONFIG_NAME_PROMPT, CHECK_VAR_CONFIG_NAME_TITLE, \
    CHECK_VAR_CONFIG_VAR_NAME_PROMPT, CHECK_VAR_CONFIG_VAR_NAME_TITLE
from src.service.system_storage.template_config_sqlite import ConfigTypeEnum
from src.service.util.import_export_util import check_template_config
from src.view.box.message_box import pop_fail
from src.view.table.table_widget.template_table_widget.template_config_table_widget import TemplateVarConfigTableWidget
from src.view.widget.template.template_config_widget import TemplateConfigWidget

_author_ = 'luwt'
_date_ = '2023/4/12 14:38'


class TemplateVarConfigWidget(TemplateConfigWidget):
    """模板变量配置表格页面控件"""

    def __init__(self):
        super().__init__(ConfigTypeEnum.template_var.value)

    def get_table_widget(self) -> TemplateVarConfigTableWidget:
        return TemplateVarConfigTableWidget(self)

    def get_check_title_prompt(self) -> tuple:
        return CHECK_VAR_CONFIG_NAME_PROMPT, CHECK_VAR_CONFIG_NAME_TITLE, \
            CHECK_VAR_CONFIG_VAR_NAME_PROMPT, CHECK_VAR_CONFIG_VAR_NAME_TITLE
