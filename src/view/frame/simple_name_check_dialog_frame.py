# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal

from src.view.frame.name_check_dialog_frame import NameCheckDialogFrame

_author_ = 'luwt'
_date_ = '2023/2/15 9:07'


class SimpleNameCheckDialogFrame(NameCheckDialogFrame):
    """简单的名称检查对话框框架，不读取数据库数据，保存功能仅发送信号，不涉及数据库修改"""
    save_signal = pyqtSignal(str)
    edit_signal = pyqtSignal(str)

    def __init__(self, parent_dialog, dialog_title, name_list, current_name=None):
        super().__init__(parent_dialog, dialog_title, name_list, current_name,
                         read_storage=False, need_help_button=False)

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def button_available(self) -> bool:
        return self.name_input.displayText() and self.name_available

    def check_data_changed(self) -> bool:
        return self.dialog_data != self.name_input.displayText()

    def save_func(self):
        # 原数据存在，说明是编辑
        if self.dialog_data:
            self.edit_signal.emit(self.name_input.displayText())
        else:
            self.save_signal.emit(self.name_input.displayText())
        self.parent_dialog.close()

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def check_edit(self):
        return self.dialog_data

    def get_old_name(self) -> str:
        return self.dialog_data

    # ------------------------------ 后置处理 end ------------------------------ #
