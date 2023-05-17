# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal

from src.service.system_storage.template_func_sqlite import TemplateFunc
from src.view.dialog.custom_dialog_abc import CustomSaveDialogABC
from src.view.frame.template.template_func_detail_dialog_frame import TemplateFuncDetailDialogFrame

_author_ = 'luwt'
_date_ = '2023/4/3 18:23'


class TemplateFuncDetailDialog(CustomSaveDialogABC):
    """模板方法详情对话框"""
    save_signal = pyqtSignal(TemplateFunc)
    edit_signal = pyqtSignal(TemplateFunc)

    def __init__(self, screen_rect, title, func_names, template_func=None):
        self.func_names = func_names
        self.template_func = template_func
        self.frame: TemplateFuncDetailDialogFrame = ...
        super().__init__(title, screen_rect)

    def resize_dialog(self):
        self.resize(self.parent_screen_rect.width() * 0.6, self.parent_screen_rect.height() * 0.7)

    def get_frame(self) -> TemplateFuncDetailDialogFrame:
        return TemplateFuncDetailDialogFrame(self, self.dialog_title, self.func_names, self.template_func)
