# -*- coding: utf-8 -*-
from src.constant.template_dialog_constant import PREVIEW_VAR_CONFIG_TITLE, PREVIEW_OUTPUT_CONFIG_TITLE
from src.view.dialog.custom_dialog_abc import CustomDialogABC
from src.view.frame.generator.dynamic_render_template_config.dyanmic_var_config_dialog_frame import \
    DynamicVarConfigDialogFrame
from src.view.frame.generator.dynamic_render_template_config.dynamic_output_config_dialog_frame import \
    DynamicOutputConfigDialogFrame
from src.view.frame.generator.dynamic_render_template_config.dynamic_template_config_dialog_frame_abc import \
    DynamicTemplateConfigDialogFrameABC

_author_ = 'luwt'
_date_ = '2023/4/6 10:40'


class TemplateConfigPreviewDialog(CustomDialogABC):
    """模板列表表格对话框"""

    def __init__(self, config_type, template_config_list):
        self.template_config_list = template_config_list
        self.frame: DynamicTemplateConfigDialogFrameABC = ...
        self.config_type = config_type
        dialog_title = PREVIEW_VAR_CONFIG_TITLE if config_type else PREVIEW_OUTPUT_CONFIG_TITLE
        super().__init__(dialog_title)

    def resize_dialog(self):
        # 当前窗口大小根据主窗口大小计算
        self.resize(self.window_geometry.width() * 0.7, self.window_geometry.height() * 0.7)

    def get_frame(self) -> DynamicTemplateConfigDialogFrameABC:
        if self.config_type:
            return DynamicVarConfigDialogFrame(self.dialog_layout, self, self.dialog_title,
                                               template_config_list=self.template_config_list,
                                               preview_mode=True)
        else:
            return DynamicOutputConfigDialogFrame(self.dialog_layout, self, self.dialog_title,
                                                  template_config_list=self.template_config_list,
                                                  preview_mode=True)
