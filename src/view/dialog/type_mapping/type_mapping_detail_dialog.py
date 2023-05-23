# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal

from src.constant.type_mapping_dialog_constant import EDIT_TYPE_MAPPING_TITLE, CREATE_TYPE_MAPPING_TITLE
from src.service.system_storage.type_mapping_sqlite import TypeMapping
from src.view.dialog.custom_dialog_abc import StackedDialogABC
from src.view.frame.type_mapping.type_mapping_detail_dialog_frame import TypeMappingDetailDialogFrame

_author_ = 'luwt'
_date_ = '2023/4/3 18:42'


class TypeMappingDetailDialog(StackedDialogABC):
    """类型映射详情对话框"""
    save_signal = pyqtSignal(TypeMapping)
    edit_signal = pyqtSignal(TypeMapping)
    override_signal = pyqtSignal(list, list)
    
    def __init__(self, type_mapping_name_tuple, type_mapping_id=None):
        self.type_mapping_name_tuple = type_mapping_name_tuple
        self.type_mapping_id = type_mapping_id
        self.frame: TypeMappingDetailDialogFrame = ...
        super().__init__(EDIT_TYPE_MAPPING_TITLE if type_mapping_id else CREATE_TYPE_MAPPING_TITLE)

    def resize_dialog(self):
        self.resize(self.window_geometry.width() * 0.7, self.window_geometry.height() * 0.7)

    def get_frame(self) -> TypeMappingDetailDialogFrame:
        return TypeMappingDetailDialogFrame(self, self.dialog_title,
                                            self.type_mapping_name_tuple,
                                            self.type_mapping_id)

    def connect_signal(self):
        super().connect_signal()
        self.frame.override_signal.connect(self.override_signal.emit)
