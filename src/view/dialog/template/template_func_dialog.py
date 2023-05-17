# -*- coding: utf-8 -*-
"""模板常用方法对话框"""

from src.constant.template_dialog_constant import TEMPLATE_FUNC_TITLE
from src.view.dialog.custom_dialog_abc import CustomDialogABC
from src.view.frame.template.template_func_dialog_frame import TemplateFuncDialogFrame

_author_ = 'luwt'
_date_ = '2023/4/3 18:41'


class TemplateFuncDialog(CustomDialogABC):
    """模板方法列表对话框"""

    def __init__(self, screen_rect):
        self.frame: TemplateFuncDialogFrame = ...
        super().__init__(TEMPLATE_FUNC_TITLE, screen_rect)

    def resize_dialog(self):
        self.resize(self.parent_screen_rect.width() * 0.6, self.parent_screen_rect.height() * 0.7)

    def get_frame(self) -> TemplateFuncDialogFrame:
        return TemplateFuncDialogFrame(self, self.dialog_title)
