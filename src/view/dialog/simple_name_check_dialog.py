# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal

from src.view.dialog.name_check_dialog import NameCheckDialog

_author_ = 'luwt'
_date_ = '2023/2/15 9:07'


class SimpleNameCheckDialog(NameCheckDialog):
    """简单的名称检查对话框，不读取数据库数据，保存功能仅发送信号，不涉及数据库修改"""
    add_name_signal = pyqtSignal(str)
    edit_name_signal = pyqtSignal(str)

    def __init__(self, screen_rect, dialog_title, name_list, current_name=None):
        super().__init__(screen_rect, dialog_title, name_list, current_name, read_storage=False)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def resize_dialog(self):
        self.resize(self.parent_screen_rect.width() * 0.3, self.parent_screen_rect.height() * 0.2)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def button_available(self) -> bool:
        return self.name_input.displayText() and self.name_available

    def check_data_changed(self) -> bool:
        return self.dialog_data != self.name_input.displayText()

    def save_func(self):
        # 原数据存在，说明是编辑
        if self.dialog_data:
            self.edit_name_signal.emit(self.name_input.displayText())
        else:
            self.add_name_signal.emit(self.name_input.displayText())
        self.close()

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def check_edit(self):
        return self.dialog_data

    def get_old_name(self) -> str:
        return self.dialog_data

    # ------------------------------ 后置处理 end ------------------------------ #
