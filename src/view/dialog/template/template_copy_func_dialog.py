# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal

from src.constant.template_dialog_constant import HAS_FUNC_TEMPLATE_LIST_TITLE
from src.view.dialog.custom_dialog_abc import CustomDialogABC
from src.view.frame.template.template_copy_func_dialog_frame import TemplateCopyFuncDialogFrame

_author_ = 'luwt'
_date_ = '2023/6/25 17:34'


class TemplateCopyFuncDialog(CustomDialogABC):
    """复制模板方法对话框"""
    copy_func_list_signal = pyqtSignal(list)

    def __init__(self, excluded_template_id, func_names):
        self.excluded_template_id = excluded_template_id
        self.func_names = func_names
        self.frame: TemplateCopyFuncDialogFrame = ...
        super().__init__(None)

    def resize_dialog(self):
        self.resize(self.window_geometry.width() * 0.6, self.window_geometry.height() * 0.7)

    def get_frame(self) -> TemplateCopyFuncDialogFrame:
        return TemplateCopyFuncDialogFrame(self.excluded_template_id, self.func_names,
                                           self, HAS_FUNC_TEMPLATE_LIST_TITLE)

    def connect_signal(self):
        self.frame.copy_func_list_signal.connect(self.copy_func_list_signal.emit)
