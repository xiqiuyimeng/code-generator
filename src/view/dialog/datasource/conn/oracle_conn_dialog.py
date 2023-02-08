# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLabel, QLineEdit

from src.constant.constant import ORACLE_DEFAULT_HOST, ORACLE_DEFAULT_PORT, ORACLE_DEFAULT_SERVICE_NAME, SERVICE_NAME_TEXT
from src.service.system_storage.conn_type import ConnType, ConnTypeEnum
from src.view.dialog.datasource.conn.internet_conn_dialog import InternetConnDialog

_author_ = 'luwt'
_date_ = '2023/2/7 11:26'


class OracleConnDialog(InternetConnDialog):

    def __init__(self, *args):
        self.service_name_label: QLabel = ...
        self.service_name_value: QLineEdit = ...
        super().__init__(*args)

    def get_conn_type(self) -> ConnType:
        return ConnTypeEnum.oracle.value

    def setup_special_conn_info_ui(self):
        self.service_name_label = QLabel(self.frame)
        self.service_name_value = QLineEdit(self.frame)
        self.ds_info_layout.addRow(self.service_name_label, self.service_name_value)

    def setup_special_conn_info_label(self):
        self.service_name_label.setText(SERVICE_NAME_TEXT)

    def setup_echo_special_conn_info_data(self):
        self.service_name_value.setText(self.dialog_data.conn_info_type.service_name)

    def collect_special_conn_info(self) -> tuple:
        return self.service_name_value.text(),

    def setup_special_conn_info_input_limit_rule(self):
        self.service_name_value.setMaxLength(50)

    def connect_special_conn_info_signal(self):
        self.service_name_value.textEdited.connect(self.check_input)

    def setup_default_value(self):
        self.host_value.setText(ORACLE_DEFAULT_HOST)
        self.port_value.setText(ORACLE_DEFAULT_PORT)
        self.service_name_value.setText(ORACLE_DEFAULT_SERVICE_NAME)
