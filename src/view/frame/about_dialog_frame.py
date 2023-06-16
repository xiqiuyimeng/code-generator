# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLabel

from src.constant.about_dialog_constant import ABOUT_INFO
from src.view.frame.dialog_frame_abc import DialogFrameABC

_author_ = 'luwt'
_date_ = '2023/6/16 16:00'


class AboutDialogFrame(DialogFrameABC):
    """关于对话框框架"""

    def __init__(self, *args):
        super().__init__(*args, need_help_button=False)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_content_ui(self):
        self.frame_layout.addWidget(QLabel(ABOUT_INFO))

    # ------------------------------ 创建ui界面 end ------------------------------ #
