# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QComboBox

from src.constant.constant import DS_TYPE_COMBO_BOX_PLACEHOLDER_TXT
from src.enum.conn_type_enum import ConnTypeEnum
from src.enum.struct_type_enum import StructTypeEnum

_author_ = 'luwt'
_date_ = '2023/2/16 13:32'


class DsTypeComboBox(QComboBox):

    def __init__(self, parent):
        super().__init__(parent)
        self.all_ds_types: list = ...
        self.setPlaceholderText(DS_TYPE_COMBO_BOX_PLACEHOLDER_TXT)
        self.fill_ds_types()

    def fill_ds_types(self):
        self.all_ds_types = list()
        for conn_type in ConnTypeEnum:
            conn_type_name = conn_type.value.display_name
            self.all_ds_types.append(conn_type_name)
            self.addItem(conn_type_name)
        for struct_type in StructTypeEnum:
            struct_type_name = struct_type.value.display_name
            self.all_ds_types.append(struct_type_name)
            self.addItem(struct_type_name)

    def echo_ds_type(self, ds_type):
        if ds_type and ds_type in self.all_ds_types:
            self.setCurrentIndex(self.all_ds_types.index(ds_type))
