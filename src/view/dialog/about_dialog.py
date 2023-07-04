# -*- coding: utf-8 -*-
from src.constant.about_dialog_constant import ABOUT_TITLE
from src.view.dialog.custom_dialog_abc import CustomDialogABC
from src.view.frame.about_dialog_frame import AboutDialogFrame

_author_ = 'luwt'
_date_ = '2023/6/16 15:57'


class AboutDialog(CustomDialogABC):
    """关于信息对话框"""

    def __init__(self):
        super().__init__(ABOUT_TITLE)

    def resize_dialog(self):
        self.resize(self.window_geometry.width() * 0.4, self.window_geometry.height() * 0.3)

    def get_frame(self) -> AboutDialogFrame:
        return AboutDialogFrame(self, self.dialog_title)
