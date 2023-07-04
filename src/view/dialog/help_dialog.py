# -*- coding: utf-8 -*-
from src.constant.help.help_constant import HELP_TITLE
from src.view.dialog.custom_dialog_abc import CustomDialogABC
from src.view.frame.help_dialog_frame import HelpDialogFrame

_author_ = 'luwt'
_date_ = '2023/6/13 18:07'


class HelpDialog(CustomDialogABC):
    """帮助对话框"""

    def __init__(self, help_info_type):
        # 当前查看的帮助信息类型
        self.help_info_type = help_info_type
        super().__init__(HELP_TITLE)

    def resize_dialog(self):
        self.resize(self.window_geometry.width() * 0.8, self.window_geometry.height() * 0.8)

    def get_frame(self) -> HelpDialogFrame:
        return HelpDialogFrame(self.help_info_type, self, self.dialog_title)
