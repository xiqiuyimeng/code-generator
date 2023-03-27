# -*- coding: utf-8 -*-
"""模板常用方法对话框"""
from src.constant.template_dialog_constant import TEMPLATE_FUNC_TITLE
from src.view.dialog.custom_dialog import CustomDialog

_author_ = 'luwt'
_date_ = '2023/3/10 10:51'


class TemplateFuncDialog(CustomDialog):

    def __init__(self, screen_rect):
        super().__init__(screen_rect, TEMPLATE_FUNC_TITLE)

    # ------------------------------ 创建ui界面 start ------------------------------ #
    def resize_dialog(self):
        self.resize(self.parent_screen_rect.width() * 0.7, self.parent_screen_rect.height() * 0.7)

    # ------------------------------ 创建ui界面 end ------------------------------ #

