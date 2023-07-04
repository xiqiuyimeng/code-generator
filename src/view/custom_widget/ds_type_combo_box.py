# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QComboBox, QLabel, QVBoxLayout

from src.constant.constant import DS_TYPE_COMBO_BOX_PLACEHOLDER_TXT
from src.service.system_storage.conn_type import ConnTypeEnum
from src.service.system_storage.struct_type import StructTypeEnum

_author_ = 'luwt'
_date_ = '2023/2/16 13:32'


class DsTypeComboBox(QComboBox):

    def __init__(self, parent):
        super().__init__(parent)
        self.placeholder_text = DS_TYPE_COMBO_BOX_PLACEHOLDER_TXT
        self.placeholder: QLabel = ...
        self.all_ds_types: list = ...
        self.fill_ds_types()
        self.setup_placeholder()
        self.connect_signal()

    def setup_placeholder(self):
        self.placeholder = QLabel()
        self.placeholder.setText(self.placeholder_text)
        self.setLayout(QVBoxLayout())
        # 左侧留出一点间距
        self.layout().setContentsMargins(5, 0, 0, 0)
        self.layout().addWidget(self.placeholder)
        self.setCurrentIndex(-1)
        # 最小宽度应该比占位符略宽一些
        self.setMinimumWidth(self.placeholder.sizeHint().width() + 30)

    def connect_signal(self):
        self.currentIndexChanged.connect(lambda idx: self.placeholder.setVisible(idx == -1))

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
