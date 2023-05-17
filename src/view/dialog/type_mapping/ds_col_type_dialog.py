# -*- coding: utf-8 -*-

from src.constant.type_mapping_dialog_constant import DS_COL_TYPE_LIST_TITLE
from src.view.dialog.custom_dialog_abc import CustomDialogABC
from src.view.frame.type_mapping.ds_col_type_dialog_frame import DsColTypeDialogFrame

_author_ = 'luwt'
_date_ = '2023/2/13 10:03'


class DsColTypeDialog(CustomDialogABC):
    """数据源列类型对话框，用以维护所有的数据类型和列类型"""

    def __init__(self, screen_rect):
        self.frame: DsColTypeDialogFrame = ...
        super().__init__(DS_COL_TYPE_LIST_TITLE, screen_rect)

    def resize_dialog(self):
        # 当前窗口大小根据主窗口大小计算
        self.resize(self.parent_screen_rect.width() * 0.7, self.parent_screen_rect.height() * 0.7)

    def get_frame(self) -> DsColTypeDialogFrame:
        return DsColTypeDialogFrame(self, self.dialog_title)
