# -*- coding: utf-8 -*-

from src.constant.template_dialog_constant import TEMPLATE_LIST_TITLE
from src.view.dialog.custom_dialog_abc import CustomDialogABC
from src.view.frame.template.template_dialog_frame import TemplateDialogFrame

_author_ = 'luwt'
_date_ = '2023/4/3 17:55'


class TemplateDialog(CustomDialogABC):
    """模板列表表格对话框"""

    def __init__(self):
        self.frame: TemplateDialogFrame = ...
        super().__init__(TEMPLATE_LIST_TITLE)

    def resize_dialog(self):
        # 当前窗口大小根据主窗口大小计算
        self.resize(self.window_geometry.width() * 0.7, self.window_geometry.height() * 0.7)

    def get_frame(self) -> TemplateDialogFrame:
        return TemplateDialogFrame(self, self.dialog_title)

