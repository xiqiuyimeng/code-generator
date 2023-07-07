# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal

from src.service.system_storage.template_func_sqlite import TemplateFunc
from src.view.dialog.custom_dialog_abc import CustomSaveDialogABC
from src.view.frame.template.template_func_detail_dialog_frame import TemplateFuncDetailDialogFrame

_author_ = 'luwt'
_date_ = '2023/4/3 18:23'


class TemplateFuncDetailDialog(CustomSaveDialogABC):
    """模板方法详情对话框"""
    save_signal = pyqtSignal(TemplateFunc)
    edit_signal = pyqtSignal(TemplateFunc)

    def __init__(self, exists_func_names, title, template_func=None):
        self.exists_func_names = exists_func_names
        self.template_func = template_func
        self.frame: TemplateFuncDetailDialogFrame = ...
        super().__init__(title)

    def resize_dialog(self):
        self.resize(self.window_geometry.width() * 0.6, self.window_geometry.height() * 0.7)

    def get_frame(self) -> TemplateFuncDetailDialogFrame:
        return TemplateFuncDetailDialogFrame(self, self.dialog_title, self.exists_func_names, self.template_func)
