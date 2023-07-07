# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal

from src.constant.template_dialog_constant import MAINTAIN_FILE_CONFIG_TITLE
from src.view.dialog.custom_dialog_abc import CustomDialogABC
from src.view.frame.template.template_maintain_file_config_frame import TemplateMaintainFileConfigFrame

_author_ = 'luwt'
_date_ = '2023/4/22 12:35'


class TemplateMaintainFileConfigDialog(CustomDialogABC):
    """模板维护文件和输出配置关系的对话框框架"""
    # 绑定文件数变化信号
    bind_file_changed = pyqtSignal()

    def __init__(self, output_config_list, unbind_file_list):
        self.output_config_list = output_config_list
        self.unbind_file_list = unbind_file_list
        self.frame: TemplateMaintainFileConfigFrame = ...
        super().__init__(MAINTAIN_FILE_CONFIG_TITLE)

    def resize_dialog(self):
        self.resize(self.window_geometry.width() * 0.6, self.window_geometry.height() * 0.7)

    def get_frame(self) -> TemplateMaintainFileConfigFrame:
        return TemplateMaintainFileConfigFrame(self.output_config_list, self.unbind_file_list,
                                               self, self.dialog_title)

    def connect_signal(self):
        self.frame.config_tree_widget.bind_file_changed.connect(self.bind_file_changed.emit)
        self.frame.file_list_widget.bind_file_changed.connect(self.bind_file_changed.emit)
