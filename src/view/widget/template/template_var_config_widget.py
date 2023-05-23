# -*- coding: utf-8 -*-
from src.service.system_storage.template_config_sqlite import ConfigTypeEnum
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
