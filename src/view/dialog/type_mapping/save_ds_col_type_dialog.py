# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal

from src.view.dialog.name_check_dialog import NameCheckDialog

_author_ = 'luwt'
_date_ = '2023/2/15 9:07'


class SaveDsColTypeDialog(NameCheckDialog):
    """添加或编辑数据源列类型对话框"""
    add_col_type_signal = pyqtSignal(str)
    edit_col_type_signal = pyqtSignal(str)

    def __init__(self, screen_rect, dialog_title, col_type_list, col_type=None):
        super().__init__(screen_rect, dialog_title, col_type_list, col_type, read_storage=False)

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
            self.edit_col_type_signal.emit(self.name_input.displayText())
        else:
            self.add_col_type_signal.emit(self.name_input.displayText())
        self.close()

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def check_edit(self):
        return self.dialog_data

    def get_old_name(self) -> str:
        return self.dialog_data

    # ------------------------------ 后置处理 end ------------------------------ #
