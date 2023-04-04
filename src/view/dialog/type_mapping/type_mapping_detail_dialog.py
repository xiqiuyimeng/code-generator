# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal

from src.constant.type_mapping_dialog_constant import TYPE_MAPPING_TITLE
from src.service.system_storage.type_mapping_sqlite import TypeMapping
from src.view.dialog.custom_dialog_abc import StackedDialogABC
from src.view.frame.type_mapping.type_mapping_detail_dialog_frame import TypeMappingDetailDialogFrame

_author_ = 'luwt'
_date_ = '2023/4/3 18:42'


class TypeMappingDetailDialog(StackedDialogABC):
    """类型映射详情对话框"""
    save_signal = pyqtSignal(TypeMapping)
    edit_signal = pyqtSignal(TypeMapping)
    
    def __init__(self, screen_rect, type_mapping_names, type_mapping_id=None):
        self.type_mapping_names = type_mapping_names
        self.type_mapping_id = type_mapping_id
        self.frame: TypeMappingDetailDialogFrame = ...
        super().__init__(TYPE_MAPPING_TITLE, screen_rect)

    def resize_dialog(self):
        self.resize(self.parent_screen_rect.width() * 0.7, self.parent_screen_rect.height() * 0.7)

    def get_frame(self) -> TypeMappingDetailDialogFrame:
        return TypeMappingDetailDialogFrame(self, self.dialog_title, self.type_mapping_names, self.type_mapping_id)
