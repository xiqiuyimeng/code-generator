# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QLabel, QLineEdit

from src.constant.ds_dialog_constant import SERVICE_NAME_TEXT, SERVICE_NAME_MAX_LENGTH_PLACEHOLDER_TEXT, \
    ORACLE_DEFAULT_HOST, ORACLE_DEFAULT_PORT, ORACLE_DEFAULT_SERVICE_NAME
from src.enum.conn_type_enum import ConnType, ConnTypeEnum
from src.view.frame.datasource.conn.internet_conn_dialog_frame import InternetConnDialogFrame

_author_ = 'luwt'
_date_ = '2023/4/3 13:44'


class OracleConnDialogFrame(InternetConnDialogFrame):
    """oracle对话框框架"""

    def __init__(self, *args):
        self.service_name_label: QLabel = ...
        self.service_name_value: QLineEdit = ...
        super().__init__(*args)

    def get_conn_type(self) -> ConnType:
        return ConnTypeEnum.oracle.value

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_special_conn_info_ui(self):
        self.service_name_label = QLabel(self)
        self.service_name_label.setObjectName('form_label')
        self.service_name_value = QLineEdit(self)
        self.ds_info_layout.addRow(self.service_name_label, self.service_name_value)

    def setup_special_conn_info_label(self):
        self.service_name_label.setText(SERVICE_NAME_TEXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def collect_special_conn_info(self) -> tuple:
        return self.service_name_value.text(),

    def connect_special_conn_info_signal(self):
        self.service_name_value.textEdited.connect(self.check_input)

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def setup_special_conn_info_input_limit_rule(self):
        self.service_name_value.setMaxLength(50)

    def setup_special_conn_info_placeholder_text(self):
        self.service_name_value.setPlaceholderText(SERVICE_NAME_MAX_LENGTH_PLACEHOLDER_TEXT)

    def setup_echo_special_conn_info_data(self):
        self.service_name_value.setText(self.dialog_data.conn_info_type.service_name)

    def setup_default_value(self):
        self.host_value.setText(ORACLE_DEFAULT_HOST)
        self.port_value.setText(ORACLE_DEFAULT_PORT)
        self.service_name_value.setText(ORACLE_DEFAULT_SERVICE_NAME)

    # ------------------------------ 后置处理 end ------------------------------ #
