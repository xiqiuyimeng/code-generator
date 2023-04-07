# -*- coding: utf-8 -*-
from src.constant.template_dialog_constant import PREVIEW_CONFIG_TITLE
from src.view.dialog.custom_dialog_abc import CustomDialogABC
from src.view.frame.generator.dynamic_template_config_dialog_frame import DynamicTemplateConfigDialogFrame

_author_ = 'luwt'
_date_ = '2023/4/6 10:40'


class TemplateConfigPreviewDialog(CustomDialogABC):
    """模板列表表格对话框"""

    def __init__(self, screen_rect, template_config_list):
        self.template_config_list = template_config_list
        self.frame: DynamicTemplateConfigDialogFrame = ...
        super().__init__(PREVIEW_CONFIG_TITLE, screen_rect)

    def resize_dialog(self):
        # 当前窗口大小根据主窗口大小计算
        self.resize(self.parent_screen_rect.width() * 0.7, self.parent_screen_rect.height() * 0.7)

    def get_frame(self) -> DynamicTemplateConfigDialogFrame:
        return DynamicTemplateConfigDialogFrame(self.dialog_layout, self, self.dialog_title,
                                                template_config_list=self.template_config_list,
                                                preview_mode=True)
