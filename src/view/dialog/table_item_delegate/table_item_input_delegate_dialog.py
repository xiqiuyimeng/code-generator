# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal

from src.constant.dialog_constant import TABLE_ITEM_INPUT_DELEGATE_TITLE
from src.view.dialog.custom_dialog_abc import CustomSaveDialogABC
from src.view.frame.table_item_delegate.table_item_input_delegate_dialog_frame import \
    TableItemInputDelegateDialogFrame

_author_ = 'luwt'
_date_ = '2023/5/19 17:31'


class TableItemInputDelegateDialog(CustomSaveDialogABC):
    """表格单元格输入框代理对话框"""
    save_signal = pyqtSignal(str)

    def __init__(self, row, col, check_text_duplicate=True, duplicate_prompt=None):
        self.check_text_duplicate = check_text_duplicate
        # 数据重复提示语
        self.duplicate_prompt = duplicate_prompt
        self.frame: TableItemInputDelegateDialogFrame = ...
        super().__init__(TABLE_ITEM_INPUT_DELEGATE_TITLE.format(row, col))

    def resize_dialog(self):
        self.resize(self.window_geometry.width() >> 1, self.window_geometry.height() >> 1)

    def get_frame(self) -> TableItemInputDelegateDialogFrame:
        return TableItemInputDelegateDialogFrame(self, self.dialog_title,
                                                 check_text_duplicate=self.check_text_duplicate,
                                                 duplicate_prompt=self.duplicate_prompt)
