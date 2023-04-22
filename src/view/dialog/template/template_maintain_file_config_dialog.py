# -*- coding: utf-8 -*-

from src.constant.template_dialog_constant import MAINTAIN_FILE_CONFIG_TITLE
from src.view.dialog.custom_dialog_abc import CustomDialogABC
from src.view.frame.template.template_maintain_file_config_frame import TemplateMaintainFileConfigFrame

_author_ = 'luwt'
_date_ = '2023/4/22 12:35'


class TemplateMaintainFileConfigDialog(CustomDialogABC):
    """模板维护文件和输出配置关系的对话框框架"""

    def __init__(self, screen_rect, output_config_list, unbind_file_list):
        self.output_config_list = output_config_list
        self.unbind_file_list = unbind_file_list
        self.frame: TemplateMaintainFileConfigFrame = ...
        super().__init__(MAINTAIN_FILE_CONFIG_TITLE, screen_rect)

    def resize_dialog(self):
        self.resize(self.parent_screen_rect.width() * 0.6, self.parent_screen_rect.height() * 0.7)

    def get_frame(self) -> TemplateMaintainFileConfigFrame:
        return TemplateMaintainFileConfigFrame(self.output_config_list, self.unbind_file_list,
                                               self, self.dialog_title)
