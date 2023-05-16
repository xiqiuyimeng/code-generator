# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal

from src.constant.template_dialog_constant import TEMPLATE_TITLE
from src.service.system_storage.template_sqlite import Template
from src.view.dialog.custom_dialog_abc import StackedDialogABC
from src.view.frame.template.template_detail_dialog_frame import TemplateDetailDialogFrame

_author_ = 'luwt'
_date_ = '2023/4/3 18:11'


class TemplateDetailDialog(StackedDialogABC):
    """模板详情对话框"""
    save_signal = pyqtSignal(Template)
    edit_signal = pyqtSignal(Template)
    override_signal = pyqtSignal(list, list)
    
    def __init__(self, screen_rect, template_names, template_id=None):
        self.template_names = template_names
        self.template_id = template_id
        self.frame: TemplateDetailDialogFrame = ...
        super().__init__(TEMPLATE_TITLE, screen_rect)

    def resize_dialog(self):
        self.resize(self.parent_screen_rect.width(), self.parent_screen_rect.height())
        # 窗口位置保持和主窗口一致
        self.setGeometry(self.parent_screen_rect)

    def get_frame(self) -> TemplateDetailDialogFrame:
        return TemplateDetailDialogFrame(self, self.dialog_title, self.template_names, self.template_id)

    def connect_signal(self):
        super().connect_signal()
        self.frame.override_signal.connect(self.override_signal.emit)
