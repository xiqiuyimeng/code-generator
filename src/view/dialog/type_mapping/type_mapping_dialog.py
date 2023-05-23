# -*- coding: utf-8 -*-

from src.constant.type_mapping_dialog_constant import TYPE_MAPPING_LIST_TITLE
from src.view.dialog.custom_dialog_abc import CustomDialogABC
from src.view.frame.type_mapping.type_mapping_dialog_frame import TypeMappingDialogFrame

_author_ = 'luwt'
_date_ = '2023/4/3 18:42'


class TypeMappingDialog(CustomDialogABC):
    """类型映射表格对话框"""

    def __init__(self):
        self.frame: TypeMappingDialogFrame = ...
        super().__init__(TYPE_MAPPING_LIST_TITLE)

    def resize_dialog(self):
        # 当前窗口大小根据主窗口大小计算
        self.resize(self.window_geometry.width() * 0.7, self.window_geometry.height() * 0.7)

    def get_frame(self) -> TypeMappingDialogFrame:
        return TypeMappingDialogFrame(self, self.dialog_title)
