# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal

from src.constant.template_dialog_constant import TEMPLATE_VAR_CONFIG_TITLE_TEXT, TEMPLATE_OUTPUT_DIR_TITLE_TEXT
from src.service.system_storage.template_config_sqlite import TemplateConfig
from src.view.dialog.custom_dialog_abc import CustomSaveDialogABC
from src.view.frame.template.template_config_dialog_frame import TemplateConfigDialogFrame

_author_ = 'luwt'
_date_ = '2023/4/3 18:15'


class TemplateConfigDialog(CustomSaveDialogABC):
    """模板配置信息对话框，不读取数据库数据，保存功能仅发送信号，不涉及数据库修改"""
    save_signal = pyqtSignal(TemplateConfig)
    edit_signal = pyqtSignal(TemplateConfig)

    def __init__(self, screen_rect, name_list, var_names, config_type, template_config=None):
        self.name_list = name_list
        self.var_names = var_names
        self.config_type = config_type
        self.template_config = template_config
        self.frame: TemplateConfigDialogFrame = ...
        dialog_title = TEMPLATE_VAR_CONFIG_TITLE_TEXT if self.config_type else TEMPLATE_OUTPUT_DIR_TITLE_TEXT
        super().__init__(dialog_title, screen_rect)

    def resize_dialog(self):
        self.resize(self.parent_screen_rect.width() * 0.5, self.parent_screen_rect.height() * 0.5)

    def get_frame(self) -> TemplateConfigDialogFrame:
        return TemplateConfigDialogFrame(self, self.dialog_title, self.name_list,
                                         self.var_names, self.config_type, self.template_config)
