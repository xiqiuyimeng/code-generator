# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal

from src.view.dialog.custom_dialog_abc import CustomSaveDialogABC
from src.view.frame.simple_name_check_dialog_frame import SimpleNameCheckDialogFrame

_author_ = 'luwt'
_date_ = '2023/4/4 9:07'


class SimpleNameCheckDialog(CustomSaveDialogABC):
    """简单的名称检查对话框，不读取数据库数据，保存功能仅发送信号，不涉及数据库修改"""
    save_signal = pyqtSignal(str)
    edit_signal = pyqtSignal(str)

    def __init__(self, exists_names, dialog_title, current_name=None):
        self.exists_names = exists_names
        self.current_name = current_name
        self.frame: SimpleNameCheckDialogFrame = ...
        super().__init__(dialog_title)

    def resize_dialog(self):
        self.resize(self.window_geometry.width() * 0.3, self.window_geometry.height() * 0.2)

    def get_frame(self) -> SimpleNameCheckDialogFrame:
        return SimpleNameCheckDialogFrame(self, self.dialog_title, self.exists_names, self.current_name)
