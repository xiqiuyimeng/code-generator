# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal

from src.constant.template_dialog_constant import CREATE_TEMPLATE_TITLE, EDIT_TEMPLATE_TITLE
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
    
    def __init__(self, exists_template_names, template_id=None):
        self.exists_template_names = exists_template_names
        self.template_id = template_id
        self.frame: TemplateDetailDialogFrame = ...
        super().__init__(EDIT_TEMPLATE_TITLE if template_id else CREATE_TEMPLATE_TITLE)

    def resize_dialog(self):
        self.resize(self.window_geometry.width(), self.window_geometry.height())
        # 窗口位置保持和主窗口一致
        self.setGeometry(self.window_geometry)

    def get_frame(self) -> TemplateDetailDialogFrame:
        return TemplateDetailDialogFrame(self, self.dialog_title, self.exists_template_names, self.template_id)

    def connect_signal(self):
        super().connect_signal()
        self.frame.override_signal.connect(self.override_signal.emit)
